from time import sleep
from typing import Any, Mapping, Optional  # for type hinting

from byteblower_test_framework.endpoint import Port  # for type hinting
from byteblower_test_framework.traffic import IPv4Frame
from byteblowerll.byteblower import Stream  # for type hinting

# Type aliases
FrameConfig = Mapping[str, Any]


class ScoutingFlow:

    @staticmethod
    def run_udp_flow(
        source: Port,
        destination: Port,
        frame_config: Optional[FrameConfig] = None,
    ) -> None:
        # Configure stream
        stream: Stream = source.bb_port.TxStreamAdd()
        stream.InterFrameGapSet(50 * 1000 * 1000)  # 50ms
        stream.NumberOfFramesSet(10)

        # Add frame to the stream
        frame = IPv4Frame(**(frame_config or {}))
        frame._add(source, destination, stream)

        # Start resolution process
        stream.Start()

        sleep(0.5)

        # Stop stream (should have stopped by itself already)
        stream.Stop()
        # Remove the stream, no longer required
        source.bb_port.TxStreamRemove(stream)
