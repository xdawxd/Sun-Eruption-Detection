from attrs import define, field


@define
class ImageHeaders:
    sun_radius: int = field(converter=int)
    image_center_x: int = field(converter=int)
    image_center_y: int = field(converter=int)
