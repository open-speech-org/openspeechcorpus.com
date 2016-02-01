# -*- coding: UTF-8 -*-
import subprocess

from openspeechcorpus.apps.core import models as core_models

def extract_length_of_audio_data(audio_data):
    """
from openspeechcorpus.apps.core import utils
a = models.AudioData.objects.all()
for b in a:
utils.extractLengthOfAudioData(b)

    """
    try:
        ffprobe_out = subprocess.Popen(
            "ffprobe " + str(audio_data.audiofile.file),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            close_fds=True
        )
        for line in ffprobe_out.stdout.readlines():
            if "Duration" in line:
                values = line.split(",")[0].split("Duration:")[1].split(":")
                duration = 3600 * float(values[0]) + 60 * float(values[1]) + float(values[2])
                ffprobe_out.stdout.close()
                ffprobe_out.pipe_cloexec()
                ffprobe_out.wait()
                print(duration)
                return duration
        ffprobe_out.stdout.close()
        ffprobe_out.pipe_cloexec()
    except IOError:
        print("0")
        return 0

def human_readable_length(length):
    """
from openspeechcorpus.apps.core import utils
utils.humanReadableLength(3663)
    """
    print length
    hours = int(length/3600)
    print hours
    minutes = int((length - 3600*hours)/60)
    print minutes
    seconds = (length - 3600*hours - 60*minutes)
    print seconds
    return str(hours) + ":" + str(minutes) + ":" + str(seconds)

def fill_empty_audiodata_length():
    """
from openspeechcorpus.apps.core import utils
utils.fill_empty_audiodata_length()
from openspeechcorpus.apps.core import models as core_models
audiodatas = core_models.AudioData.objects.filter(length=0).order_by("-id")
audiodatas.count()
    """
    audiodatas = core_models.AudioData.objects.filter(length=0).order_by("-id")
    for audiodata in audiodatas:
        audiodata.length = extract_length_of_audio_data(audiodata)
        audiodata.save()

def get_total_audio_recorder():
    """
from openspeechcorpus.apps.core import utils
utils.get_total_audio_recorder()
    """

    audiodatas = core_models.AudioData.objects.all()
    total_audio = 0
    for audiodata in audiodatas:
        total_audio += audiodata.length
    return human_readable_length(total_audio)


def get_total_audios_from_user(user_id):
    """
from openspeechcorpus.apps.core import utils
utils.get_total_audios_from_user(12312)
    """

    audiodatas = core_models.AnonymousAudioData.objects.filter(user=user_id)
    total_audio = 0
    for audiodata in audiodatas:
        total_audio += audiodata.audio.length
    return human_readable_length(total_audio)

def migrate_records_from_user_to_new_user(old_user_id, new_user_id):
    """
from openspeechcorpus.apps.core import utils
utils.migrate_records_from_user_to_new_user(6,11)
    """
    try:
        old_user = core_models.AnonymousUserProfile.objects.get(pk=old_user_id)
        new_user = core_models.AnonymousUserProfile.objects.get(pk=new_user_id)
        user_audiodatas = core_models.AnonymousAudioData.objects.filter(user=old_user)
        for user_audiodata in user_audiodatas:
            user_audiodata.user = new_user
            user_audiodata.save()
        datamigration = core_models.AudioDatasMigration(
            old_user=old_user,
            new_user=new_user
        )
        datamigration.save()
        return True

    except core_models.AnonymousUserProfile.DoesNotExist:
        return False

def assign_orphan_audio_to_user(first_id,anonymous_user_id):
    """
from openspeechcorpus.apps.core import utils
utils.assign_orphan_audio_to_user()
    """
    audios = core_models.AudioData.objects.filter(id__gt=first_id)
    audios.count()
    orphan_audios = []
    for audio in audios:
        try:
            core_models.AnonymousAudioData.objects.get(audio=audio)
        except core_models.AnonymousAudioData.DoesNotExist:
            orphan_audios.append(audio)

    len(orphan_audios)

    user = core_models.AnonymousUserProfile.objects.get(pk=anonymous_user_id)
    for orphan_audio in orphan_audios:
        core_models.AnonymousAudioData.objects.create(audio=orphan_audio, user=user)





