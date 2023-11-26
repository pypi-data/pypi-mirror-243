# Press Shift+F10 to execute this program.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
# import os
from pathlib import Path
import glob
import astropy.io.fits as pyfits
import numpy as np

from dateutil import parser
import datetime
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from edge_finding_utilities import find_best_r_only_from_min_max_size, subFrameAdjusted

verbose = False
progress_factor = 50

__version__ = "1.0.0"

def parse_flash_times(flash_times_str):
    format_ok = False
    parts = flash_times_str.split(' ')
    if len(parts) == 4:
        sub_parts_1 = parts[0].split('-')
        sub_parts_2 = parts[1].split(':')
        sub_parts_3 = parts[2].split('-')
        sub_parts_4 = parts[3].split(':')
        if len(sub_parts_1) == len(sub_parts_2) == len(sub_parts_3) == len(sub_parts_4) == 3:
            format_ok = True

    if not format_ok:
        print(f"\nInvalid format for flash-times. Given was {flash_times_str}\n\n"
              f" - a correct example: 2023-10-09 13:45:11  2023-10-09 13:47:33")
        return False
    else:
        return True

def process_fits_video(args):
    global verbose

    verbose = args.verbose
    if verbose: print(f"Entered process_fits_video() with fits path: {args.fits[0]}")

    # Finally, we need to add to all the FITS files DATE-OBS (timestamp header)
    fitsFiles = glob.glob(f'{args.fits[0]}/*.fits')
    print(f"Found: {len(fitsFiles)} fits files in {args.fits[0]}")

    # Now we sort them into frame order (often needed)
    fitsFiles.sort()

    # Read the fits files to pick out cpu timestamps. We use to get a good estime of exposure without requiring
    # the user to enter it. We also get a list of the cpu timestamps that we will use in the droppedFrameAnalysis() procedure
    cpuTimestamps, cpuTimestampComment = getCpuTimestamps(fits_files=fitsFiles)

    print(f"\nNumber of cpu timestamps found: {len(cpuTimestamps)}")

    exposure = None

    if len(cpuTimestamps) > 0:
        ans = droppedFrameAnalysis(cpu_timestamps=cpuTimestamps)
        if ans[0] == 'ok':
            frame_time = ans[1]
            if verbose: print(f"Frame time: {frame_time:0.5f}")
            exposure = frame_time * 1000  # Convert to milliseconds
            if verbose: print(f"exposure derived from cpuTimestamps: {exposure:0.3f} milliseconds")
        else:
            print(ans[1])
            exit(-1)

    flashLightcurve = extract_flash_lightcurve(fitsFiles)

    processFlashLightCurve(flashLightcurve, args, exposure, cpuTimestamps, cpuTimestampComment)

    plotFlashLightCurve(flashLightcurve, args)

def extract_flash_lightcurve(fits_files):
    lightcurve = []

    for frame_file in fits_files:
        image = pyfits.getdata(frame_file, 0)
        image = image.astype('int64')
        lightcurve.append(np.sum(image))

    return lightcurve

def plotFlashLightCurve(flashLightCurve, args):
    plt.figure(figsize=(10,5), num="Flash lightcurve")
    plt.title(f"From: {args.fits[0]}\nflash times: {args.flash_times}")
    plt.plot(flashLightCurve, '-', color='lightgray')
    plt.plot(flashLightCurve, '.')
    plt.xlabel('reading number')
    plt.ylabel('total frame intensity')
    plt.show()

def getCpuTimestamps(fits_files):
    global verbose, progress_factor

    progress = 0
    print(f'\nProcessing file to get cpu timestamps (each * is {progress_factor} files): ', end='')

    cpu_timestamps = []
    for frame_file in fits_files:
        progress += 1
        if progress % progress_factor == 0:
            print('*', end='')
        with pyfits.open(frame_file, output_verify='ignore') as hdul:
            hdul[0].verify('ignore')
            hdr = hdul[0].header
            try:
                cpu_timestamp = hdr['DATE-SYS']  # From a previous run
                cpu_timestamps.append(cpu_timestamp)
                cpu_timestamp_comment = hdr.comments['DATE-SYS']
            except KeyError:
                try:
                    cpu_timestamp = hdr['DATE-END']  # For SharpCap v3.2.6482.0, 32 bit
                    cpu_timestamps.append(cpu_timestamp)
                    cpu_timestamp_comment = hdr.comments['DATE-END']
                except KeyError:  # This will happen if it's not SharpCap v3 (so no DATE-END card)
                    try:
                        date_obs_value = hdr['DATE-OBS']
                        date_obs_comment = hdr.comments['DATE-OBS'] # For SharpCap v4.0.9499.0, 64 bit
                        if date_obs_comment.startswith('System'):
                            cpu_timestamps.append(date_obs_value)
                            cpu_timestamp_comment = hdr.comments['DATE-OBS']
                    except KeyError:
                        pass
    return cpu_timestamps, cpu_timestamp_comment

def SharpCapSafe_strptime(ts, format_str):
    # This bit of shenanigans is needed because SharpCap has 7 digits in the fraction seconds (<= 6 is normal)
    parts = ts.split('.')
    if not len(parts) == 2:  # This is a fatal format error
        return 'error', f"Error in timestamp format: {ts}"
    if len(parts[1]) > 6:
        parts[1] = parts[1][:6]
    ts_fixed = f"{parts[0]}.{parts[1]}"
    try:
        ts_time = datetime.datetime.strptime(ts_fixed, format_str)
        return 'ok', ts_time
    except ValueError as e:
        return 'error', f"Error in timestamp format: {ts_fixed} {e}"


def droppedFrameAnalysis(cpu_timestamps):

    if len(cpu_timestamps) > 0:
        cpu_frame_times = []
        for ts in cpu_timestamps:
            ans = SharpCapSafe_strptime(ts, '%Y-%m-%dT%H:%M:%S.%f')  # ans = ('err_msg', time)
            if ans[0] == 'ok':
                cpu_frame_times.append(ans[1])
            else:
                return ans
        deltas = []
        for i in range(1, len(cpu_frame_times)):
            deltas.append((cpu_frame_times[i] - cpu_frame_times[i-1]).total_seconds())  # noqa
        # Now we look for unusual gaps
        median_gap = np.median(deltas)
        msg = [
            f"avg delta: {np.mean(deltas):0.6f}  median delta: {np.median(deltas):0.6f}  "
            f"max delta: {np.max(deltas):0.6f}  min delta: {np.min(deltas):0.6f}"
        ]
        # print(msg[0])
        for i, delta in enumerate(deltas):
            if delta > 1.5 * median_gap:
                msg.append(f"At frame {i} there is a gap that is {delta/median_gap:0.1f} times normal.")
        if len(msg) == 1:
            msg.append(f"Gap analysis of cpu timestamps indicate that there were no dropped frames.")
        print(f"\nDropped frame detection report:")
        for line in msg:
            print(f"... {line}")
        return 'ok', np.median(deltas)
    else:
        return 'error', 'No cpu timestamps found'

# def processFlashLightCurve(ts1='2023-11-11 16:29:20+00:00', ts2='2023-11-11 16:29:21+00:00'):
def processFlashLightCurve(flashLightCurve, args, exposure, cpuTimestamps, cpuTimestampComment):
    global verbose, progress_factor

    flash_time_str = args.flash_times

    # Split the flash_times into ts1 and ts1
    parts = flash_time_str.split(' ')
    if not len(parts) == 4:
        print(f"Error in timestamp format - given was: {flash_time_str}")
        return

    ts1 = parts[0] + ' ' + parts[1]
    ts2 = parts[2] + ' ' + parts[3]

    if verbose: print(f"ts1: {ts1}  ts2: {ts2}")

    fitsFolderPath = args.fits[0]

    # The values for ts1 and ts1 are for test purposes only. Used with a 100 ms exposure, and a 1010 frame
    # manual record (1000 frames - 100 seconds - between flash edges), the timing will be accurate
    # ts2 = 2023-11-11 16:31:10+00:00

    # For a 110 frame manual record, use ts2 = 2023-11-11 16:29:30+00:00

    # For a 110 frame manual record at 10 ms exposure, use ts2 = 2023-11-11 16:29:21+00:00

    t1 = parser.parse(ts1)  # Create a datetime object
    t2 = parser.parse(ts2)

    if verbose: print(t1,t2, '\n')

    seconds_apart = (t2-t1).total_seconds()

    if verbose: print(f"timestamp difference: {seconds_apart} seconds")

    if verbose: print(f"Length of flashLightCurve: {len(flashLightCurve)}")
    # if verbose: print(flashLightCurve)

    # Initially we extract parameters from the entire set of points. Those values may be 'off' a bit if
    # viewing conditions are very different as the recording progresses.
    # We will assume that that is happening and refine the calcultions by isolating flash light curve points
    # from the beginning, and then from the end of the recording, and recalculating using only nearby points.

    # First estimation:
    max_flash_level = np.max(flashLightCurve)
    min_flash_level = np.min(flashLightCurve)
    mid_flash_level = (max_flash_level + min_flash_level) // 2

    # Find first flash region using the 'first estimation' values
    first_flash = []

    state = 'accumulateBottom'

    for value in flashLightCurve:
        if state == 'accumulateBottom':
            if value < mid_flash_level:
                first_flash.append(value)
            else:
                state = 'accumulateTop'

        if state == 'accumulateTop':
            if value >= mid_flash_level:
                first_flash.append(value)
            else:
                break

    if verbose: print(f"\nfirst_flash: {first_flash}")

    ans, interpolated_r = findFlashEdgeInterpolatedPosition(first_flash)
    if not ans == 'ok':
        print(f"findFlashEdgeTimeCorrection() returned: {ans}")
        exit()

    if verbose: print(f"Found that the first flash edge started at frame {interpolated_r:0.4f}")
    first_flash_subframe_value = interpolated_r

    time_correction_first = (interpolated_r - int(interpolated_r)) * exposure
    if verbose: print(f"time_correction first_flash: {time_correction_first:0.2f} microseconds")

    tf1 = t1 - datetime.timedelta(microseconds=round(time_correction_first))
    if verbose: print(tf1)

    # Now we need to find the last flash. To do that, we'll work backwards

    state = 'traverseRightBottom'
    k = len(flashLightCurve) - 1  # We use k to iterate backwards through the flashLightCurve
    righthand_index = k
    while True:
        value = flashLightCurve[k]
        if state == 'traverseRightBottom':
            if value < mid_flash_level:  # we're still in the flash off portion of the tail
                k -= 1
            else:
                state = 'traverseTop'
                last_flash_top_end = k  # Save this because we need to know where the top of the last flash ends
                bottom_length = righthand_index - k

        if state == 'traverseTop':
            if value >= mid_flash_level:  # We're still in the flash on portion
                k -= 1
            else:
                state = 'traverseLeftBottom'

        if state == 'traverseLeftBottom':
            k -= bottom_length  # noqa No need to do anything other than backup to give a normal flash off zone
            last_flash_bottom_start = k
            break

        if k <= 0:
            print('\nData error: Could not find the terminating flash\n')

    last_flash = flashLightCurve[last_flash_bottom_start:last_flash_top_end+1]  # noqa
    if verbose: print(f"last_flash: {last_flash}")

    ans, interpolated_r = findFlashEdgeInterpolatedPosition(last_flash)
    if not ans == 'ok':
        print(f"findFlashEdgeTimeCorrection() returned: {ans}")
        exit()

    if verbose: print(f"Found that the last flash edge started at frame {last_flash_bottom_start + interpolated_r:0.4f}")
    last_flash_subframe_value = interpolated_r + last_flash_bottom_start

    time_correction_last = (interpolated_r - int(interpolated_r)) * exposure

    if verbose: print(f"time_corrrection last_flash: {time_correction_last:0.2f} microseconds")

    tf2 = t2 - datetime.timedelta(microseconds=round(time_correction_last))

    # Because datetime objects have 1 microsecond resolution (not enough to reliably extrapolate over 1000 to 10000 points),
    # we calculate our own delta with more than 1 microsecond resolution
    precison_time_difference = (t2 - t1).total_seconds() * 1_000_000 + time_correction_first - time_correction_last
    precision_delta = precison_time_difference / (last_flash_subframe_value - first_flash_subframe_value)  # noqa
    if verbose: print(f"precision_time_difference: {precison_time_difference:0.2f} microseconds")
    if verbose: print(f"precision_delta: {precision_delta:0.2f} microseconds")

    # Now we need to calculate a timestamp list.

    # We calculate a well-averaged frame time from the timestamped readings...
    frameTime = (tf2 - tf1) / (last_flash_subframe_value - first_flash_subframe_value)   # noqa
    # if verbose: print(type(frameTime), frameTime)

    timestamps = []
    t0 = tf1 - datetime.timedelta(microseconds=first_flash_subframe_value * precision_delta)
    for i in range(len(flashLightCurve)):
        tn = t0 + datetime.timedelta(microseconds=i * precision_delta)
        ts_str = tn.strftime('%Y-%m-%dT%H:%M:%S.%f')
        timestamps.append(ts_str)
        # print(f"{i:03d}: {ts_str}")

    # Finally, we need to add to all the FITS files DATE-OBS (timestamp header)
    fitsFiles = glob.glob(f'{fitsFolderPath}/*.fits')

    # Now we sort them. This not needed fo src, but may be important for the planned utility.
    # In any case, it doesn't hurt.
    fitsFiles.sort()

    i = 0
    progress = 0
    print(f'\nAdding GPS timestamps to each fits file (each * is {progress_factor} files): ', end='')

    import warnings
    warnings.filterwarnings("ignore")

    QHYtimestamps = []
    for frame_file in fitsFiles:
        progress += 1
        if progress %progress_factor == 0:
            print('*', end='')
        with pyfits.open(frame_file, mode='update', output_verify='ignore') as hdul:
            hdul[0].verify('ignore')
            hdr = hdul[0].header
            if cpuTimestamps:
                hdr['DATE-SYS'] = cpuTimestamps[i]
                hdr.comments['DATE-SYS'] = cpuTimestampComment
            QHYtimestamps.append(hdr['DATE-OBS'])  # Only used for testing with a flash-tagged QHY recording
            hdr['DATE-OBS'] = timestamps[i]
            hdr.comments['DATE-OBS'] = 'GPS from PyFlashToGPS ' + __version__
            i += 1
    print(f'\n...GPS timestamp addition completed.')

    if args.QHY174GPS:  # Run a QHY test
        t_diff = []
        for i in range(len(QHYtimestamps)):
            t_us = SharpCapSafe_strptime(timestamps[i], '%Y-%m-%dT%H:%M:%S.%f')
            t_qhy = SharpCapSafe_strptime(QHYtimestamps[i], '%Y-%m-%dT%H:%M:%S.%f')
            t_diff.append((t_us[1] - t_qhy[1]).total_seconds())  # noqa
        print(f'\nComparison of QHY174GPS timestamps with flash-tag derived GPS timestamps:\n'
              f'... statistics of deltas where delta[i] = flash_tag_time[i] - QHY_time[i] (seconds) ...\n'
              f'    mean(delta): {np.mean(t_diff):0.6f}  max(delta): {np.max(t_diff):0.6f}  min(delta): {np.min(t_diff):0.6f}')

def findFlashEdgeInterpolatedPosition(flash_to_analyze):
    min_event = len(flash_to_analyze) // 4
    max_event = 3 * min_event
    left = 0
    right = len(flash_to_analyze) - 1
    y = np.array(flash_to_analyze).astype('float64')

    # Use PyOTE routines to find edge position
    error_code, d, r, b, a, sigmaB, sigmaA, metric = find_best_r_only_from_min_max_size(
        y=y, left=left, right=right, min_event=min_event, max_event=max_event
    )

    if not error_code == 'ok':
        # Failed to find R - probably a program error
        print(f"During processFlashLightCurve() find_best_r returned error code: {error_code}")
        return 'failed to find R edge', None

    if d == -1:  # The normal return for an R only event
        d = None

    subDandR, new_b, new_a, newSigmaB, newSigmaA = subFrameAdjusted(  # noqa
        eventType='Ronly',
        cand=(d, r),
        B=b, A=a,
        sigmaB=sigmaB, sigmaA=sigmaA,
        yValues=flash_to_analyze,
        left=left, right=right
    )

    interloplated_r = subDandR[1]
    return 'ok', interloplated_r

def timestamper():
    global verbose

    arg_parser = argparse.ArgumentParser(description="A utility to add GPS accurate timestamps to flash-tagged FITS videos.",
                                         prog='PyFlashToGPS')

    # group = ts_parser.add_mutually_exclusive_group()

    arg_parser.add_argument("flash_times", help='UTC times for first and last flash. Example: "2023-09-02 13:45:10 2023-09-02 13:47:05"'
                                                ' (the quotes are needed!)')

    arg_parser.add_argument("--verbose", action='store_true',
                           help="Verbose output (used during development)")

    arg_parser.add_argument("--QHY174GPS", action='store_true',
                            help="If file came from a QHY174GPS camera, a comparison report is made between the GPS timestamps")

    arg_parser.add_argument("--fits", type=str, nargs=1,
                        metavar="FITS_path", default=None,
                        help="Full path to FITS folder")

    # arg_parser.add_argument("--exposure", type=str, nargs=1,
    #                         metavar="exposure", default=None,
    #                         help="exposure time in milliseconds")

    # group.add_argument("--adv2", type=str, nargs=1,
    #                     metavar="ADV2_path", default=None,
    #                     help="Full path to ADV2 file")

    args = arg_parser.parse_args()
    verbose = args.verbose

    # if args.exposure is None:
    #     print('\nAn exposure time (in milliseconds) must be entered. Use the --exposure option for this.\n')
    #     return

    if parse_flash_times(args.flash_times):
        if args.fits is not None and verbose: print(f"FITS folder path given: {args.fits[0]}")
    else:
        return

    if args.fits is not None:
        fits_folder_path = Path(args.fits[0])
        if not fits_folder_path.exists():
            print(f"Cannot find fits folder: {args.fits[0]}")
            exit(-1)
        else:
            if verbose: print(f"FITS folder path given exists - proceeding to process_fits_video.")
            process_fits_video(args)

    # if args.adv2 is not None:
    #     adv2_file_path = Path(args.adv2[0])
    #     if not adv2_file_path.exists():
    #         print(f"Cannot find adv2 file: {args.adv2[0]}")
    #         exit()
    #     elif verbose:
    #         print(f"ADV2 file has been found.")

if __name__ == '__main__':
    timestamper()
