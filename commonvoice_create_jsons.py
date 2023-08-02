import os
import argparse
import json
import random
import csv
from pydub import AudioSegment

def main(args):
    data = []
    percent = args.percent
    clips_directory = os.path.join(args.save_json_path, 'clips')

    if not os.path.exists(clips_directory):
        os.makedirs(clips_directory)
    
    with open(args.file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        length = sum(1 for _ in reader)  # Count the number of lines in the CSV
        index = 1

        if args.convert:
            print(str(length) + " files found")

        for row in reader:
            file_name = row['path']
            filename = file_name.rpartition('.')[0] + ".wav"
            text = row['sentence']

            if args.convert:
                data.append({
                    "key": os.path.join('clips', filename),
                    "text": text
                })

                print(f"converting file {index}/{length} to wav", end="\r")

                src = os.path.join(args.file_path.rpartition('/')[0], 'clips', file_name)
                dst = os.path.join(args.save_json_path, 'clips', filename)

                sound = AudioSegment.from_mp3(src)
                sound.export(dst, format="wav")
                index = index + 1
            else:
                data.append({
                    "key": os.path.join('clips', file_name),
                    "text": text
                })

    random.shuffle(data)
    print("creating JSON's")

    train_data = data[:int(length * (1 - percent / 100))]
    test_data = data[int(length * (1 - percent / 100)):]

    with open(os.path.join(args.save_json_path, 'train.json'), 'w') as f:
        json.dump(train_data, f, indent=4)

    with open(os.path.join(args.save_json_path, 'test.json'), 'w') as f:
        json.dump(test_data, f, indent=4)

    print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility script to convert Common Voice into WAV and create training and test JSON files for speech recognition.")
    parser.add_argument('--file_path', type=str, default=None, required=True,
                        help='path to one of the .tsv files found in cv-corpus')
    parser.add_argument('--save_json_path', type=str, default=None, required=True,
                        help='path to the dir where the json files are supposed to be saved')
    parser.add_argument('--percent', type=int, default=10, required=False,
                        help='percent of clips put into test.json instead of train.json')
    parser.add_argument('--convert', default=True, action='store_true',
                        help='says that the script should convert mp3 to wav')
    parser.add_argument('--not-convert', dest='convert', action='store_false',
                        help='says that the script should not convert mp3 to wav')

    args = parser.parse_args()

    main(args)
