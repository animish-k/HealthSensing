
# Personal Baseline Anomaly Detector

## Purpose

This module flags heart-rate readings that deviate from an
individual's reference baseline using a statistical z-score.

It is an experimental anomaly detector, not a medical diagnostic tool.

## Function

`detect_anomalies(readings, baseline_readings, threshold=3.0)`

### Inputs

- `readings`: non-empty, one-dimensional sequence of finite numeric
  heart-rate readings in beats per minute (bpm).
- `baseline_readings`: sequence of at least two finite numeric
  readings representing the individual's reference period.
- `threshold`: positive finite absolute z-score threshold.
  Defaults to `3.0`.

### Output

A Pandas DataFrame with one row per input reading:

- `heart_rate_bpm`: input heart-rate reading.
- `z_score`: deviation from the baseline mean, divided by the
  baseline sample standard deviation.
- `detected_anomaly`: `1` when the absolute z-score exceeds the
  threshold; otherwise `0`.

### Validation

The function raises `ValueError` for empty inputs, non-finite values,
multidimensional inputs, insufficient baseline measurements, a
zero-variation baseline, or an invalid threshold.

### Missing data

Missing and non-finite values are not treated as normal readings.
The caller must validate and handle missing data before calling
the detector.

### Limitations

The detector currently evaluates heart rate only. It does not
combine environmental signals, learn a supervised classifier, or
diagnose health conditions.

The default threshold has not been medically validated. Performance
must be evaluated on suitable real data before drawing conclusions
about real-world effectiveness.
