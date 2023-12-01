import logging
from typing import Optional

from pymavlink.dialects.v20.ardupilotmega import (
    MAV_CMD_DO_SET_MODE,
    MAV_CMD_NAV_LAND,
    MAV_CMD_NAV_TAKEOFF,
    MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED,
)

from albatros.enums import CommandResult, ConnectionType, CopterFlightModes, MavFrame
from albatros.telem import ComponentAddress
from albatros.telem.message_models import PositionTargetLocalNED
from albatros.uav import UAV

from .outgoing.commands import (
    get_command_long_message,
    get_set_position_target_local_ned_message,
)

logger = logging.getLogger(__name__)


class Copter(UAV):
    """Class that provides actions the copter can perform."""

    def __init__(
        self,
        uav_addr: ComponentAddress = ComponentAddress(system_id=1, component_id=1),
        my_addr: ComponentAddress = ComponentAddress(system_id=1, component_id=191),
        connection_type: ConnectionType = ConnectionType.DIRECT,
        device: Optional[str] = "udpin:0.0.0.0:14550",
        baud_rate: Optional[int] = 115200,
        host: Optional[str] = None,
        port: Optional[int] = None,
    ) -> None:
        super().__init__(
            uav_addr,
            my_addr,
            connection_type,
            device,
            baud_rate,
            host,
            port,
        )
        self.set_parameter("FENCE_ENABLE", 1)

    def set_mode(self, mode: CopterFlightModes) -> bool:
        """Set system mode.

        :param mode: ardupilot flight mode you want to set.
        """
        msg = get_command_long_message(
            target_system=self.uav_addr.system_id,
            target_component=self.uav_addr.component_id,
            command=MAV_CMD_DO_SET_MODE,
            param1=1,
            param2=mode.value,
        )

        self.driver.send(msg)
        logger.info("Set mode command sent")

        if self.wait_command_ack().result != CommandResult.ACCEPTED:
            return False
        return True

    def takeoff(self, alt_m: float, yaw: float = float("NaN")) -> bool:
        """Takeoff copter. Set Guided mode and send takeoff command.

        :param alt_m: The altitude to which the Copter is to ascend
        :param yaw: Yaw angle (if magnetometer present), ignored without magnetometer.
            NaN to use the current system yaw heading mode (e.g. yaw towards next waypoint,
            yaw to home, etc.).
        """
        self.set_parameter("FENCE_ENABLE", 0)

        if not self.set_mode(CopterFlightModes.GUIDED):
            logger.error("Unable to set GUIDED mode, aborting")
            return False

        msg = get_command_long_message(
            self.uav_addr.system_id,
            self.uav_addr.component_id,
            MAV_CMD_NAV_TAKEOFF,
            param4=yaw,
            param7=alt_m,
        )

        self.driver.send(msg)
        logger.info("Takeoff command sent")

        if self.wait_command_ack().result != CommandResult.ACCEPTED:
            return False
        return True

    def land(self) -> bool:
        """Land copter in the place where it is currently located. Works only in `GUIDED` mode.

        :returns: True if command was accepted
        """

        msg = get_command_long_message(
            self.uav_addr.system_id,
            self.uav_addr.component_id,
            MAV_CMD_NAV_LAND,
        )

        self.driver.send(msg)
        logger.info("Land command sent")

        if self.wait_command_ack().result != CommandResult.ACCEPTED:
            return False
        return True

    def fly_to_local_position(
        self,
        north_m: float,
        east_m: float,
        alt_m: float,
        yaw_rad: float = 0,
        yaw_rate_rad: float = 0,
    ) -> bool:
        """Move copter to the NED location relative to origin of the coordinate system.

        :param north_m: meters to the north,
        :param east_m: meters to the east,
        :param alt_m: altitude in meters relative to start point.
        :param yaw_rad: yaw setpoint (rad)
        :param yaw_rate: yaw rate setpoint (rad/s)

        Works only in Guided mode.
        """

        msg = get_set_position_target_local_ned_message(
            self.uav_addr.system_id,
            self.uav_addr.component_id,
            north_m,
            east_m,
            alt_m,
            yaw_rad,
            yaw_rate_rad,
            MavFrame.LOCAL_NED,
        )

        self.driver.send(msg)
        logger.info("Flight to point command sent.")

        if (
            self.request_message(MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED)
            != CommandResult.ACCEPTED
        ):
            return False

        try:
            target = self.wait_message(PositionTargetLocalNED())
            if target.x == north_m and target.y == east_m:
                return True
            return False

        except TimeoutError:
            return False

    def fly_to_local_offset_position(
        self,
        north_m: float,
        east_m: float,
        alt_m: float,
        yaw_rad: float = 0,
        yaw_rate_rad: float = 0,
    ) -> bool:
        """Move copter to the NED location relative to the current position.

        :param north_m: meters to the north,
        :param east_m: meters to the east,
        :param alt_m: altitude in meters relative to start point.
        :param yaw_rad: yaw setpoint (rad)
        :param yaw_rate: yaw rate setpoint (rad/s)

        Works only in Guided mode.
        """

        msg = get_set_position_target_local_ned_message(
            self.uav_addr.system_id,
            self.uav_addr.component_id,
            north_m,
            east_m,
            alt_m,
            yaw_rad,
            yaw_rate_rad,
            MavFrame.LOCAL_OFFSET_NED,
        )

        self.driver.send(msg)
        logger.info("Flight to point command sent.")

        if (
            self.request_message(MAVLINK_MSG_ID_POSITION_TARGET_LOCAL_NED)
            != CommandResult.ACCEPTED
        ):
            return False

        try:
            target = self.wait_message(PositionTargetLocalNED())
            if target.x == north_m and target.y == east_m:
                return True
            return False

        except TimeoutError:
            return False
