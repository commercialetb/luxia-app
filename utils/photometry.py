import re, math
def parse_ldt(ldt_file):
    """
    Semplice parser per file Eulumdat (.ldt).
    Restituisce un dizionario con alcuni campi utili quando reperibili.
    Nota: parser semplificato per MVP. Non copre ogni possibile variante LDT.
    """
    raw = ldt_file.read()
    # ensure string
    if isinstance(raw, bytes):
        text = raw.decode('latin1', errors='ignore')
    else:
        text = str(raw)
    lines = text.splitlines()

    result = {"raw_lines_count": len(lines)}

    # Name usually in first line
    result['name'] = lines[0].strip() if lines else "unknown"

    # Try to find sequences of numbers: the LDT contains numeric blocks.
    nums = []
    for ln in lines:
        # extract floats/ints from line
        found = re.findall(r"[-+]?\d*\.\d+|\d+", ln)
        if found:
            nums.append([float(x) for x in found])

    # Heuristic: often line ~23 contains total luminous flux; try to find any reasonable lumen number (>100)
    total_flux = None
    for arr in nums:
        for val in arr:
            if val > 100 and val < 100000:  # plausible lumen range
                total_flux = val
                break
        if total_flux:
            break
    result['total_luminous_flux'] = total_flux

    # Try to get intensity distributions: find largest numeric arrays and take as intensities
    sorted_by_len = sorted(nums, key=lambda x: len(x), reverse=True)
    if sorted_by_len:
        intensities = sorted_by_len[0]  # best guess
        result['intensities_guess'] = intensities[:200]  # limit size
        # compute Imax and attempt to estimate angle where I <= 0.5*Imax
        Imax = max(intensities) if intensities else None
        result['Imax'] = Imax
        if Imax:
            half = 0.5 * Imax
            # assume angles evenly spaced from 0 to 180
            n = len(intensities)
            for i, I in enumerate(intensities):
                if I <= half:
                    angle_deg = (i / max(1, n-1)) * 180.0
                    # semi-angle δ is angle where I falls to 0.5 Imax -> take that
                    result['semi_angle_deg_guess'] = angle_deg
                    break

    return result


def estimate_beam_angle_from_ldt(parsed_ldt):
    """
    Return estimated semi-angle delta in degrees from parsed LDT dict.
    """
    if not parsed_ldt:
        raise ValueError("No parsed LDT provided")
    if parsed_ldt.get('semi_angle_deg_guess'):
        return parsed_ldt['semi_angle_deg_guess']
    # fallback: use default
    raise ValueError("Unable to estimate angle from this .LDT file (parser fallback)")

def calculate_beam_spread(h, hc, delta_deg):
    """
    Compute beam width (diameter) on calculation plane:
    b = (h - hc) * tan(delta) * 2
    where delta is semi-angle in degrees.
    """
    return (h - hc) * math.tan(math.radians(delta_deg)) * 2.0
