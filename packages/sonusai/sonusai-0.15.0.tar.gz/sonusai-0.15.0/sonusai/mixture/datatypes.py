from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from dataclasses_json import DataClassJsonMixin

AudioT: TypeAlias = npt.NDArray[np.float32]
AudiosT: TypeAlias = list[AudioT]

ListAudiosT: TypeAlias = list[AudiosT]

Truth: TypeAlias = npt.NDArray[np.float32]
Segsnr: TypeAlias = npt.NDArray[np.float32]

AudioF: TypeAlias = npt.NDArray[np.complex64]
AudiosF: TypeAlias = list[AudioF]

EnergyT: TypeAlias = npt.NDArray[np.float32]
EnergyF: TypeAlias = npt.NDArray[np.float32]

Feature: TypeAlias = npt.NDArray[np.float32]

Predict: TypeAlias = npt.NDArray[np.float32]

# Json type defined to maintain compatibility with DataClassJsonMixin
Json: TypeAlias = dict | list | str | int | float | bool | None


class DataClassSonusAIMixin(DataClassJsonMixin):
    def __str__(self):
        return f'{self.to_dict()}'

    # Override DataClassJsonMixin to remove dictionary keys with values of None
    def to_dict(self, encode_json=False) -> dict[str, Json]:
        def del_none(d):
            if isinstance(d, dict):
                for key, value in list(d.items()):
                    if value is None:
                        del d[key]
                    elif isinstance(value, dict):
                        del_none(value)
                    elif isinstance(value, list):
                        for item in value:
                            del_none(item)
            elif isinstance(d, list):
                for item in d:
                    del_none(item)
            return d

        return del_none(super().to_dict(encode_json))


@dataclass(frozen=True)
class TruthSetting(DataClassSonusAIMixin):
    config: Optional[dict] = None
    function: Optional[str] = None
    index: Optional[list[int]] = None

    def __hash__(self):
        return hash(self.to_json())

    def __eq__(self, other):
        return isinstance(other, TruthSetting) and hash(self) == hash(other)


TruthSettings: TypeAlias = list[TruthSetting]
NumberStr: TypeAlias = float | int | str
OptionalNumberStr: TypeAlias = Optional[NumberStr]
OptionalListNumberStr: TypeAlias = Optional[list[NumberStr]]
EQ: TypeAlias = tuple[float | int, float | int, float | int]


@dataclass
class AugmentationRule(DataClassSonusAIMixin):
    normalize: OptionalNumberStr = None
    pitch: OptionalNumberStr = None
    tempo: OptionalNumberStr = None
    gain: OptionalNumberStr = None
    eq1: OptionalListNumberStr = None
    eq2: OptionalListNumberStr = None
    eq3: OptionalListNumberStr = None
    lpf: OptionalNumberStr = None
    ir: OptionalNumberStr = None
    mixup: Optional[int] = 1


AugmentationRules: TypeAlias = list[AugmentationRule]


@dataclass
class Augmentation(DataClassSonusAIMixin):
    normalize: Optional[float] = None
    pitch: Optional[float] = None
    tempo: Optional[float] = None
    gain: Optional[float] = None
    eq1: Optional[EQ] = None
    eq2: Optional[EQ] = None
    eq3: Optional[EQ] = None
    lpf: Optional[float] = None
    ir: Optional[int] = None


Augmentations: TypeAlias = list[Augmentation]


@dataclass(frozen=True)
class UniversalSNRGenerator:
    is_random: bool
    _raw_value: float | str

    @property
    def value(self) -> float:
        if self.is_random:
            from .augmentation import evaluate_random_rule

            return float(evaluate_random_rule(str(self._raw_value)))

        return float(self._raw_value)


class UniversalSNR(float):
    def __new__(cls, value: float, is_random: bool = False):
        return float.__new__(cls, value)

    def __init__(self, value: float, is_random: bool = False) -> None:
        float.__init__(value)
        self._is_random = bool(is_random)

    @property
    def is_random(self) -> bool:
        return self._is_random


# @dataclass(frozen=True)
# class UniversalSNR:
#     is_random: bool
#     value: float
#
#     def __lt__(self, other) -> bool:
#         return self.value < other.value


@dataclass
class TargetFile(DataClassSonusAIMixin):
    name: str
    samples: int
    truth_settings: TruthSettings
    class_balancing_augmentation: Optional[AugmentationRule] = None
    level_type: Optional[str] = None

    @property
    def duration(self) -> float:
        from .constants import SAMPLE_RATE

        return self.samples / SAMPLE_RATE


TargetFiles: TypeAlias = list[TargetFile]


@dataclass
class AugmentedTarget(DataClassSonusAIMixin):
    target_id: int
    target_augmentation_id: int


AugmentedTargets: TypeAlias = list[AugmentedTarget]


@dataclass
class NoiseFile(DataClassSonusAIMixin):
    name: str
    samples: int

    @property
    def duration(self) -> float:
        from .constants import SAMPLE_RATE

        return self.samples / SAMPLE_RATE


NoiseFiles: TypeAlias = list[NoiseFile]
ClassCount: TypeAlias = list[int]

GeneralizedIDs: TypeAlias = str | int | list[int] | range


@dataclass(frozen=True)
class TruthFunctionConfig(DataClassSonusAIMixin):
    feature: str
    mutex: bool
    num_classes: int
    target_gain: float
    config: Optional[dict] = None
    function: Optional[str] = None
    index: Optional[list[int]] = None


@dataclass
class GenMixData:
    targets: Optional[AudiosT] = None
    target: Optional[AudioT] = None
    noise: Optional[AudioT] = None
    mixture: Optional[AudioT] = None
    truth_t: Optional[Truth] = None
    segsnr_t: Optional[Segsnr] = None


@dataclass
class GenFTData:
    feature: Optional[Feature] = None
    truth_f: Optional[Truth] = None
    segsnr: Optional[Segsnr] = None


@dataclass
class ImpulseResponseData:
    name: str
    sample_rate: int
    data: AudioT

    @property
    def length(self) -> int:
        return len(self.data)


ImpulseResponseFiles: TypeAlias = list[str]


@dataclass(frozen=True)
class SpectralMask(DataClassSonusAIMixin):
    f_max_width: int
    f_num: int
    t_max_width: int
    t_num: int
    t_max_percent: int


SpectralMasks: TypeAlias = list[SpectralMask]


@dataclass
class Target(DataClassSonusAIMixin):
    file_id: Optional[int] = None
    augmentation: Optional[Augmentation] = None
    gain: Optional[float] = None


Targets = list[Target]


@dataclass
class Noise(DataClassSonusAIMixin):
    file_id: Optional[int] = None
    augmentation: Optional[Augmentation] = None
    offset: Optional[int] = None


@dataclass
class Mixture(DataClassSonusAIMixin):
    name: Optional[str] = None
    noise: Optional[Noise] = None
    noise_snr_gain: Optional[float] = None
    samples: Optional[int] = None
    snr: Optional[UniversalSNR] = None
    spectral_mask_id: Optional[int] = None
    spectral_mask_seed: Optional[int] = None
    target_snr_gain: Optional[float] = None
    targets: Optional[Targets] = None

    @property
    def noise_id(self) -> int:
        return self.noise.file_id

    @property
    def target_id(self) -> list[int]:
        return [target.file_id for target in self.targets]


Mixtures = list[Mixture]


@dataclass(frozen=True)
class TransformConfig:
    N: int
    R: int
    bin_start: int
    bin_end: int
    ttype: str


@dataclass(frozen=True)
class FeatureGeneratorConfig:
    feature_mode: str
    num_classes: int
    truth_mutex: bool


@dataclass(frozen=True)
class FeatureGeneratorInfo:
    decimation: int
    stride: int
    step: int
    num_bands: int
    ft_config: TransformConfig
    eft_config: TransformConfig
    it_config: TransformConfig


@dataclass
class MixtureDatabaseConfig(DataClassSonusAIMixin):
    asr_manifest: list[str] = field(default_factory=list)
    class_balancing: Optional[bool] = False
    class_labels: Optional[list[str]] = None
    class_weights_threshold: Optional[list[float]] = None
    feature: Optional[str] = None
    impulse_response_files: Optional[ImpulseResponseFiles] = None
    mixtures: Optional[Mixtures] = None
    noise_mix_mode: Optional[str] = 'exhaustive'
    noise_files: Optional[NoiseFiles] = None
    num_classes: Optional[int] = None
    spectral_masks: Optional[SpectralMasks] = None
    target_files: Optional[TargetFiles] = None
    truth_mutex: Optional[bool] = None
    truth_reduction_function: Optional[str] = None
