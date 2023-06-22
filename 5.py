import speech_recognition as sr
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from googletrans import Translator
#pip install googletrans==3.1.0a0
translator = Translator()

#from googletrans import LANGUAGES
#for lang_code, lang_name in LANGUAGES.items():
    #print(f"{lang_code}: {lang_name}")

r = sr.Recognizer()

inputLang = {
    1 : "ru-RU", #русский
    2 : "en-EN", #англ
    3 : "fr-FR", #франц
    4 : "zh-CN", #китайский (некорректное отображение субтитров)
    5 : "it-IT", #итал
    6 : "ja-JP", #японский (некорректное отображение субтитров)
    7 : "kk-ТЗЗ", #казахский
    8 : "pl-PL", #польский
    9 : "pt-BR", #португальский
    10 : "es-ES", #испанский
    11 : "sv-SE", #шведский
    12 : "tr-TR", #турецкий
}

language1 = int(input("Выберите язык исходного видео: \n 1 - Русский \n 2 - Английский \n 3 - Французский \n 4 - Китайский \n 5 - Итальянский "
                      "\n 6 - Японский \n 7 - Казахский \n 8 - Польский \n 9 - Португальский \n 10 - Испанский \n 11 - Шведский \n 12 - Турецкий \n "))
input_lang = inputLang.get(language1)

outputLang = {

 1 : "hy", # armenian
 2 : "az", # azerbaijani
 3 : "be", # belarusian
 4 : "bg", # bulgarian
 5 : "zh-cn", # chinese (simplified)
 6 : "hr", # croatian
 7 : "cs", # czech
 8 : "da", # danish
 9 : "nl", # dutch
 10 : "en", # english
 11 : "et", # estonian
 12 : "fi", # finnish
 13 : "fr", # french
 14 : "ka", # georgian
 15 : "de", # german
 16 : "el", # greek
 17 : "iw", # hebrew
 18 : "hi", # hindi
 19 : "hmn", # hmong
 20 : "hu" ,# hungarian
 21 : "ga", # irish
 22 : "it",  # italian
 23 : "ja", # japanese
 24 : "kk", # kazakh
 25 : "ko", # korean
 26 : "ky", # kyrgyz
 27 : "lv", # latvian
 28 : "lt", # lithuanian
 29 : "mn", # mongolian
 30 : "no", # norwegian
 31 : "pl", # polish
 32 : "pt", # portuguese
 33 : "ro", # romanian
 34 : "ru", # russian
 35 : "sr", # serbian
 36 : "sk", # slovak
 37 : "sl", # slovenian
 38 : "es", # spanish
 39 : "sv", # swedish
 40 : "tg", # tajik
 41 : "th", # thai
 42 : "tr", # turkish
 43 : "ug", # uyghur
 44 : "uz", # uzbek
 45 : "vi" # vietnamese

}

language2 = int(input("Выберите язык субтитров: \n 1 - Армянский \n 2 - Азербайджанский \n 3 - Белорусский \n 4 - Болгарский \n 5 - Китайский"
                      " \n 6 - Хорватский \n 7 - Чешский \n 8 - Датский \n 9 - Голландский \n 10 - Английский"
                      "\n 11 - Эстонский \n 12 - Финский \n 13 - Французский \n 14 - Грузинский \n 15 - Немецкий"
                      "\n 16 - Греческий \n 17 - Иврит \n 18 - Хинди \n 19 - Хмонг \n 20 - Венгерский"
                      "\n 21 - Ирландский \n 22 - Итальянский \n 23 - Японский \n 24 - Казахский \n 25 - Корейский"
                      "\n 26 - Киргизский \n 27 - Латышский \n 28 - Литовский \n 29 - Монгольский \n 30 - Норвежский"
                      "\n 31 - Польский \n 32 - Португальский \n 33 - Румынский \n 34 - Русский \n 35 - Сербский"
                      "\n 36 - Словацкий \n 37 - Словенский \n 38 - Испанский \n 39 - Шведский \n 40 - Таджикский"
                      "\n 41 - Тайский \n 42 - Турецкий \n 43 - Уйгурский \n 44 - Узбекский \n 45 - Вьетнамский \n"))
output_lang = outputLang.get(language2)

sizeSubtitles = int(input("Введите размер субтитров (рекомендуемый размер - 16): \n"))

# Извлекаем аудио из видео файла
nameVideo = "video.mp4"
formatVideo = nameVideo.split(".")[-1]  # .mp4 .webm .ogv
video = VideoFileClip(nameVideo)
audio = video.audio
audio.write_audiofile("audio.wav")
filename = 'audio.wav'

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 300,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=1000,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    # process each chunk
    subtitles = []
    timer = 0
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the folder_name directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language= input_lang)
                text = f"{text.capitalize()}. "
                res = translator.translate(text, dest =output_lang)
                print(chunk_filename, ":", res.text)
                print(audio_chunk.duration_seconds)
                # create a subtitle clip for the chunk
                subtitle_clip = TextClip(txt=res.text, fontsize=sizeSubtitles, size=(600,130), color='orange', bg_color='transparent', method='caption')
                subtitle_clip = subtitle_clip.set_duration(
                    audio_chunk.duration_seconds).set_start(timer, change_end=True)
                timer+=audio_chunk.duration_seconds

                subtitles.append(subtitle_clip)
            except sr.UnknownValueError as e:
                print("Error:", str(e))

    # combine all subtitle clips into one video clip
    subtitles_clip = CompositeVideoClip(subtitles)
    # overlay the subtitle clip onto the original video
    result = video.set_audio(None).set_duration(subtitles_clip.duration).set_fps(30).set_audio(audio)
    result = result.set_audio(audio)
    result = CompositeVideoClip([result, subtitles_clip.set_position(('center', 'bottom'))])
    return result

result = get_large_audio_transcription(filename)
result.write_videofile("result."+formatVideo, fps=30)