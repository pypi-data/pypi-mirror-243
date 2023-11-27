import threed_optix.utils.vars as v
from skimage.transform import rescale as sk_scale

def process_headers(headers_num):

    data_kind_mapping = v.DATA_KINDS_MAPPING
    polarization_mapping = v.POLARIZATION_MAPPING

    analysis_kind = headers_num['analysis kind'][0]
    data_kind = headers_num['data kind'][0]
    polarization_kind = headers_num['polarization kind'][0]
    num_hits = headers_num['num_hits'][0]
    num_wavelengths = headers_num['num_wavelengths'][0]
    resolution_x = headers_num['resolution_x'][0]
    resolution_y = headers_num['resolution_y'][0]
    resolution = (resolution_x, resolution_y)
    data_kind_value = data_kind_mapping.get(data_kind)
    polarization_kind_value = polarization_mapping.get(polarization_kind)

    headers = {
        "analysis_kind": analysis_kind,
        "data_kind": data_kind_value,
        "polarization_kind": polarization_kind_value,
        "num_hits": num_hits,
        "num_wavelengths": num_wavelengths,
        "resolution": resolution
    }

    return headers

def print_completed_failed(completed, failed, message):
    completed_ = completed.copy()
    failed_ = failed.copy()
    print(f"{message} successfully: {len(completed_)}, failed: {len(failed_)}")

def reorganize_analysis_results_dict(results):
    results = list(results).copy()
    polarization_dict = {}
    for result in results:
        polarization_kind = result['metadata']['polarization_kind'].split('_')[0].capitalize()
        modified_res = result.copy()
        del modified_res['metadata']['polarization_kind']
        polarization_dict[polarization_kind] = modified_res
    return polarization_dict

def upscale(results, height, width):
    scale_height = height / results.shape[0]
    scale_width = width / results.shape[1]
    sk_upscale_scale = max(scale_height, scale_width)
    if sk_upscale_scale > 1:
        upscaled_results = sk_scale(results, scale = sk_upscale_scale, anti_aliasing=False)
        return upscaled_results
    return results
