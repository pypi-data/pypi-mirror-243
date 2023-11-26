from opensr_test.utils import hq_histogram_matching


def spectral_histogram_matching(input_tensor, target_tensor):
    """
    Histogram matching for spectral bands
    """
    return hq_histogram_matching(input_tensor, target_tensor)
