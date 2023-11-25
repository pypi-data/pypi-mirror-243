"""A linker for the monistode set of ISAs."""
from dataclasses import dataclass
import itertools

from monistode_binutils_shared import (
    Executable,
    ObjectManager,
    PlacedBinary,
    Segment,
    Symbol,
    SymbolRelocation,
)
from monistode_binutils_shared.bytearray import ByteArray


@dataclass
class PlacedSegment:
    """A segment that has been placed into memory."""

    offset: int
    segment: Segment

    def symbols(self) -> tuple[Symbol, ...]:
        """Get the symbols in the segment."""
        return self.segment.symbols(self.offset)

    def get_data(self, data: ByteArray, at: int, bits: int) -> tuple[int, int]:
        """Get data at a specific offset.

        Args:
            data: The data to get from.
            at: The offset to get the data from.
            bits: The number of bits to get.

        Returns:
            The extracted data and the number of bits lost.
        """
        n_bytes = -(-bits // data._byte)
        lost_bits = n_bytes * data._byte - bits
        extracted = 0
        for byte_offset in range(n_bytes):
            extracted <<= data._byte
            extracted |= data[at + byte_offset]
        return extracted, lost_bits

    def set_data(self, data: ByteArray, at: int, bits: int, value: int) -> None:
        """Set data at a specific offset.

        Args:
            data: The data to set.
            at: The offset to set the data at.
            bits: The number of bits to set (will be rounded up to the nearest byte).
            value: The value to set the data to.
        """
        n_bytes = -(-bits // data._byte)
        for byte_offset in range(n_bytes):
            data[at + n_bytes - byte_offset - 1] = value & 0xFF
            value >>= data._byte

    def get_relocation_target(
        self, relocation: SymbolRelocation, symbols: tuple[Symbol, ...]
    ) -> int:
        """Get the relocation target.

        Args:
            relocation: The relocation to get the target of.
            symbols: The symbols to get the target from.

        Returns:
            The relocation target, relative if necessary.
        """
        candidates = [
            symbol
            for symbol in symbols
            if symbol.name == relocation.symbol.name
            and symbol.location.section == relocation.symbol.section_name
        ]
        if len(candidates) == 0:
            raise ValueError(
                f"Could not find symbol {relocation.symbol.name} "
                f"in section {relocation.symbol.section_name}"
            )
        if len(candidates) > 1:
            raise ValueError(
                f"Found multiple symbols {relocation.symbol.name} "
                f"in section {relocation.symbol.section_name}"
            )
        relative_to = (
            (self.offset + relocation.location.offset) if relocation.relative else 0
        )

        return candidates[0].location.offset - relative_to

    def with_relocations(self, targets: tuple[Symbol, ...]) -> ByteArray:
        """Get the segment with relocations applied."""
        data: ByteArray = self.segment.data()
        for relocation in self.segment.relocations:
            relocation: SymbolRelocation
            original, lost_bits = self.get_data(
                data, relocation.offset, relocation.size
            )
            target = self.get_relocation_target(relocation, targets)
            new_address = target + original >> lost_bits
            if new_address < 0:
                new_address += 1 << relocation.size
            new_address &= (1 << relocation.size) - 1
            relocation_mask = ((1 << relocation.size) - 1) << lost_bits
            new_address <<= lost_bits
            new_address |= original & ~relocation_mask
            self.set_data(data, relocation.offset, relocation.size, new_address)
        return data

    def asbinary(self, targets: tuple[Symbol, ...]) -> PlacedBinary:
        """Get the segment as a binary."""
        return PlacedBinary(
            self.with_relocations(targets),
            self.offset,
            self.segment.size,
            self.segment.flags,
        )


class Linker:
    """A linker for the monistode set of ISAs."""

    def __init__(self) -> None:
        """Initialize the linker."""
        self.objects: list[ObjectManager] = []

    def add_object(self, obj: ObjectManager) -> None:
        """Add an object to the linker."""
        self.objects.append(obj)

    def add_binary(self, binary: bytes) -> None:
        """Add a binary to the linker."""
        self.add_object(ObjectManager.from_bytes(binary))

    def link(
        self,
        target: Executable,
        harvard: bool = False,
        max_merge_distance: int = 0,
    ) -> None:
        """Link the objects together into an executable.

        Args:
            harvard: Whether to link the objects as a Harvard architecture.
                Allows data and code to be stored in the same memory space.
                Defaults to False.
        """
        segments = self.form_segments()
        placed_segments = self.place_segments(segments, harvard)
        symbols = self.form_symbols(placed_segments)
        entry_point = self.get_entry_point(symbols)
        binaries = [
            placed_segment.asbinary(symbols) for placed_segment in placed_segments
        ]
        self.merge_binaries(binaries, max_merge_distance)

        target.clear(
            harvard,
            entry_point,
        )
        for binary in binaries:
            target.append_segment(binary)

    def form_segments(self) -> tuple[Segment, ...]:
        """Form segments from the objects."""
        return sum(
            (
                section.segments()
                for section in itertools.chain.from_iterable(self.objects)
            ),
            (),
        )

    def place_segments(
        self, segments: tuple[Segment, ...], harvard: bool = False
    ) -> tuple[PlacedSegment, ...]:
        """Place the segments into memory.

        Args:
            segments: The segments to place.
            harvard: Whether to place the segments as a Harvard architecture.
                Allows data and code to be stored in the same memory space.
                Defaults to False.

        Returns:
            The placed segments.
        """
        text_segments = self.place_text_segments(segments)
        text_offset = (
            0
            if harvard
            else max(
                (segment.offset + segment.segment.size for segment in text_segments),
                default=0,
            )
        )
        data_segments = self.place_data_segments(segments, text_offset)
        return text_segments + data_segments

    def place_text_segments(
        self, segments: tuple[Segment, ...]
    ) -> tuple[PlacedSegment, ...]:
        """Place the text segments into memory.

        Args:
            segments: The segments to place.

        Returns:
            The placed segments.
        """
        offset = 0
        placed_segments = []
        for segment in segments:
            if segment.flags.executable:
                placed_segments.append(PlacedSegment(offset, segment))
                offset += segment.size
        return tuple(placed_segments)

    def place_data_segments(
        self, segments: tuple[Segment, ...], offset: int
    ) -> tuple[PlacedSegment, ...]:
        """Place the data segments into memory.

        Args:
            segments: The segments to place.
            offset: The offset to place the segments at.

        Returns:
            The placed segments.
        """
        placed_segments = []
        for segment in segments:
            if not segment.flags.executable:
                placed_segments.append(PlacedSegment(offset, segment))
                offset += segment.size
        return tuple(placed_segments)

    def form_symbols(self, segments: tuple[PlacedSegment, ...]) -> tuple[Symbol, ...]:
        """Form symbols from the segments.

        Args:
            segments: The segments to form symbols from.

        Returns:
            The formed symbols.
        """
        symbols = []
        for segment in segments:
            symbols.extend(segment.symbols())
        return tuple(symbols)

    def get_entry_point(self, symbols: tuple[Symbol, ...]) -> int:
        """Get the entry point of the program.

        Args:
            symbols: The symbols to search for the entry point.

        Returns:
            The entry point of the program.
        """
        try:
            return next(
                symbol.location.offset
                for symbol in symbols
                if symbol.name == "_start" and symbol.location.section == "text"
            )
        except StopIteration:
            raise RuntimeError("No entry point found")

    def merge_binaries(
        self, binaries: list[PlacedBinary], max_merge_distance: int
    ) -> None:
        # For else is used to break out of the loop when no more merges can be done
        if len(binaries) == 1:
            return
        while True:
            for first, second in itertools.permutations(binaries):
                if (
                    first.offset + first.disk_size - second.offset < max_merge_distance
                    and first.flags == second.flags
                ):
                    first.extend(second, max_merge_distance)
                    binaries.remove(second)
                    break
            else:
                break
