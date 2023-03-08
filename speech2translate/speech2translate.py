from python_translator import Translator
import speech_recognition as sr
import subprocess
import sys
import io


def audio2text(path=r'./sample.mp3', lang='zh-TW'):
    print('Converting to WAV')  # Speech converter can process only WAV
    subprocess.call(['ffmpeg', '-y', '-i', path, 'tmp.wav'], stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

    r = sr.Recognizer()
    with sr.AudioFile('tmp.wav') as source:
        audio_text = r.listen(source)
        try:
            print('Converting to text')
            # create a text trap and redirect stdout
            sys.stdout = io.StringIO()
            # convert WAV to text
            text = r.recognize_google(audio_text, language=lang)
            # restore stdout function
            sys.stdout = sys.__stdout__
            print('Recorded:', text)
            return text
        except Exception:
            print('Sorry.. run again...')


def translate(txt, from_lang='chinese', to_lang='english'):
    translator = Translator()
    result = translator.translate(txt, to_lang, from_lang)
    print('Translated:', result)
    return result


if __name__ == "__main__":
    txt = audio2text(sys.argv[1]) if len(sys.argv) > 1 else audio2text()
    translate(txt)
