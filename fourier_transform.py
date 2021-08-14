import numpy as np
import numpy.fft as nf
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt
import cv2

# 一维傅里叶变换, 以数字音频处理为例
def audio_fourier():
    # 读取音频文件, 获取音频文件基本信息: 采样个数、采用周期
    # 与每个采样的声音信号值, 绘制音频时域的时间/位移图像
    sample_rate, noised_sigs = wf.read('./assets/noised.wav')
    print(sample_rate)
    print(noised_sigs.shape)
    times = np.arange(noised_sigs.size) / sample_rate

    plt.figure('Filter')
    plt.subplot(221)
    plt.title('Time Domain', fontsize = 16)
    plt.ylabel('Signal', fontsize = 12)
    plt.tick_params(labelsize = 10)
    plt.grid(linestyle = ':')
    plt.plot(times[:178], noised_sigs[:178], c = 'orangered', label = 'Noised')
    plt.legend()

    # 使用傅里叶变换, 获取音频频域信息, 绘制音频频域的频域/能量图像
    freqs = nf.fftfreq(times.size, times[1] - times[0])
    complex_array = nf.fft(noised_sigs)
    pows = np.abs(complex_array)

    plt.subplot(222)
    plt.title('Frequency Domain', fontsize = 16)
    plt.ylabel('Power', fontsize = 12)
    plt.tick_params(labelsize = 10)
    plt.grid(linestyle = ':')
    # 指数增长坐标画图
    plt.semilogy(freqs[freqs > 0], pows[freqs > 0], c = 'limegreen', label = 'Noised')
    plt.legend()

    # 将低频噪声去除后绘制音频频域的频率/能量图像
    fund_freq = freqs[pows.argmax()]
    noised_indices = np.where(freqs != fund_freq)
    filter_complext_array = complex_array.copy()
    filter_complext_array[noised_indices] = 0
    filter_pows = np.abs(filter_complext_array)

    plt.subplot(223)
    plt.xlabel('Frequency', fontsize = 12)
    plt.ylabel('Power', fontsize = 12)
    plt.tick_params(labelsize = 10)
    plt.grid(linestyle = ':')
    plt.plot(freqs[freqs >= 0], filter_pows[freqs >= 0], c = 'dodgerblue', label = 'Filter')
    plt.legend()

    # 基于逆向傅里叶变换, 生成新的音频信号, 绘制音频时域的时间/位移图像
    filter_sigs = nf.ifft(filter_complext_array).real
    plt.subplot(224)
    plt.xlabel('Time', fontsize = 12)
    plt.ylabel('Signal', fontsize = 12)
    plt.tick_params(labelsize = 10)
    plt.grid(linestyle = ':')
    plt.plot(times[:178], filter_sigs[:178], c = 'hotpink', label = 'Filter')
    plt.legend()

    plt.show()

    wf.write('./assets/filter.wav', sample_rate, filter_sigs)

# 二维傅里叶变换, 以数字图像处理为例
def image_fourier():
    img = cv2.imread('./assets/shanghai.jpg', flags = 0)

    f = nf.fft2(img)
    fshift = nf.fftshift(f)

    fimg = np.log(np.abs(fshift))

    plt.figure()
    plt.subplot(331)
    plt.title('Original Image')
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img, 'gray')

    plt.subplot(332)
    plt.title('Fourier Transform')
    plt.xticks([])
    plt.yticks([])
    plt.imshow(fimg, 'gray')

    ishift = nf.ifftshift(fshift)
    ifimg = nf.ifft2(ishift)

    
    plt.subplot(333)
    plt.title('Inverted Fourier Transform')
    plt.xticks([])
    plt.yticks([])
    plt.imshow(np.abs(ifimg), 'gray')

    # 低通滤波
    # 原始频域图 低通滤波频域图 低通滤波后的图像
    height, width = img.shape
    center = height // 2, width // 2
    mask = np.zeros((height, width))
    mask[center[0] - 50: center[0] + 50, center[1] - 50: center[1] + 50] = 1

    low_filter_img = fshift * mask
    low_filter_img_ishift = nf.ifftshift(low_filter_img)
    low_filter_img_spatial = nf.ifft2(low_filter_img_ishift)

    plt.subplot(334)
    plt.title('Frequency Image')
    plt.xticks([])
    plt.yticks([])
    plt.imshow(fimg, 'gray')

    plt.subplot(335)
    plt.title('Low Pass Filter')
    plt.xticks([])
    plt.yticks([])
    low_filter_img = np.log(np.abs(low_filter_img))
    low_filter_img[low_filter_img == -np.inf] = 0
    plt.imshow(low_filter_img , 'gray')

    plt.subplot(336)
    plt.title('Back To Spaital Domain')
    plt.xticks([])
    plt.yticks([])
    plt.imshow(np.abs(low_filter_img_spatial), 'gray')

    # 高通滤波
    # 原始频域图 高通滤波频域图 高通滤波后的图像
    mask = np.ones((height, width))
    mask[center[0] - 50: center[0] + 50, center[1] - 50: center[1] + 50] = 0
    high_filter_img = fshift * mask
    high_filter_img_ishift = nf.ifftshift(high_filter_img)
    high_filter_img_spatial = nf.ifft2(high_filter_img_ishift)

    plt.subplot(337)
    plt.title('Frequency Image')
    plt.xticks([])
    plt.yticks([])
    plt.imshow(fimg, 'gray')

    plt.subplot(338)
    plt.title('High Pass Filter')
    plt.xticks([])
    plt.yticks([])
    plt.imshow(np.log(np.abs(high_filter_img)), 'gray')

    plt.subplot(339)
    plt.title('Back To Spatial Domain')
    plt.xticks([])
    plt.yticks([])
    plt.imshow(np.abs(high_filter_img_spatial), 'gray')


    plt.show()


def main():
    image_fourier()

if __name__ == '__main__':
    main()