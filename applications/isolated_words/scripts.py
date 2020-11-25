import random
import shutil
from applications.isolated_words import models


models.IsolatedWordSpeech.objects.all().count()
def extract_1_records_from_each_word():
    all_words = models.IsolatedWord.objects.all()
    list_words = list()
    for word in all_words:
        records_by_word = models.IsolatedWordSpeech.objects.filter(isolated_word=word)
        number_of_recordings = records_by_word.count()
        random_index = random.randint(0, number_of_recordings - 1)
        recording = records_by_word[random_index]
        try:
            shutil.copy2(
                f'/mnt/16810535-988c-440c-a794-1c9b98899844/master_thesis/corpus/01_open_speech_corpus/words_wav/words/{recording.audio.id}.wav',
                '/mnt/16810535-988c-440c-a794-1c9b98899844/master_thesis/corpus/01_open_speech_corpus/words_annotations/wav'
            )
            list_words.append(f"{recording.audio.id},{recording.isolated_word.text.encode().decode('UTF-8', errors='ignore')}\n")
        except FileNotFoundError:
            print(f"File {recording.audio.id} does not exists")
    with open('/mnt/16810535-988c-440c-a794-1c9b98899844/master_thesis/corpus/01_open_speech_corpus/words_annotations/word_map.txt', 'w+', encoding='UTF-8') as f:
        f.writelines(list_words)


extract_1_records_from_each_word()
