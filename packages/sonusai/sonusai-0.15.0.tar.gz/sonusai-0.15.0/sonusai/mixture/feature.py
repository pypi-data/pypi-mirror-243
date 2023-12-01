from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import Feature


def get_feature_from_audio(audio: AudioT, feature: str) -> Feature:
    from dataclasses import asdict

    import numpy as np
    from pyaaware import FeatureGenerator

    from .augmentation import get_pad_length
    from .datatypes import FeatureGeneratorConfig
    from .datatypes import TransformConfig
    from .helpers import forward_transform
    from .truth import truth_reduction

    num_classes = 1
    truth_mutex = False
    truth_reduction_function = 'max'

    fg_config = FeatureGeneratorConfig(feature_mode=feature,
                                       num_classes=num_classes,
                                       truth_mutex=truth_mutex)
    fg = FeatureGenerator(**asdict(fg_config))
    feature_step_samples = fg.ftransform_R * fg.decimation * fg.step

    audio = np.pad(array=audio, pad_width=(0, get_pad_length(len(audio), feature_step_samples)))
    samples = len(audio)
    audio_f = forward_transform(audio, TransformConfig(N=fg.ftransform_N,
                                                       R=fg.ftransform_R,
                                                       bin_start=fg.bin_start,
                                                       bin_end=fg.bin_end,
                                                       ttype=fg.ftransform_ttype))

    transform_frames = samples // fg.ftransform_R
    feature_frames = samples // feature_step_samples

    truth_t = np.empty((samples, num_classes), dtype=np.float32)

    data = np.empty((feature_frames, fg.stride, fg.num_bands), dtype=np.float32)

    feature_frame = 0
    for transform_frame in range(transform_frames):
        indices = slice(transform_frame * fg.ftransform_R, (transform_frame + 1) * fg.ftransform_R)
        fg.execute(audio_f[transform_frame], truth_reduction(truth_t[indices], truth_reduction_function))

        if fg.eof():
            data[feature_frame] = fg.feature()
            feature_frame += 1

    return data
