# 用于保存音频
import wave
#数学库
import numpy as np
import matplotlib.pyplot as plt

#中文支持和布局调整
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['figure.figsize']=(15,8)

plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=0.5, hspace=0.5)

def saveAudio(filename,data,params):
    with wave.open(filename + '.wav', 'wb') as wavfile:
        print(params)
        wavfile.setparams(params)
        wavfile.writeframes(bytes(data))

def wavread(path):
    wavfile = wave.open(path, "rb")
    params = wavfile.getparams()
    print(params)

    framesra, frameswav = params[2], params[3]
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.frombuffer(datawav, dtype=np.short)
    datause.shape = -1, 2
    datause = datause.T
    time = np.arange(0, frameswav) * (1.0 / framesra)
    return datause, time, params

path = r"spring.wav"
wavdata, wavtime, params = wavread(path)

noise=np.random.rand(len(wavdata[0]))

noise_music = wavdata.copy() + noise
saveAudio("加噪后_spring", noise_music, params)

transformed=np.fft.fft2(noise_music)

avg1 = np.max(abs(transformed[0][1:]))/10000
avg2 = np.max(abs(transformed[1][1:]))/10000
transformed[0][np.where(abs(transformed[0])<=avg1)]=0+0j
transformed[1][np.where(abs(transformed[1])<=avg2)]=0+0j

noise_music = np.fft.ifft2(transformed).astype(int) #astype(int)很重要，过滤掉浮点过小信号

plt.subplot(231)
plt.title("原音频时序")
plt.plot(wavdata[0][4000:4500])

plt.subplot(232)
plt.title("原音频频域")
plt.plot(np.fft.fft(wavdata[0][4000:4200]))

plt.subplot(233)
plt.title("噪声音频时序")
plt.plot(noise_music[0][4000:4500])

plt.subplot(234)
plt.title("噪声音频频域")
plt.plot(np.fft.fft(noise_music[0][4000:4200]))

plt.show()
saveAudio("还原后_spring", noise_music, params)
















































































