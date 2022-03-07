# video_quality_measurement

The video bits encoded with LDPC codes are further used to measure quality of video in terms of PSNR  and VMAF.

video is encoded with H264 codec and results are observed for three different bit rates.

PSNR: -
Ratio of maximum power of transmitted signal to total noise power of introduced noise is termed peak signal to noise ratio or PSNR. For video codec, transmitted signal is called as original information bit while noise is considered as error introduced due to channel compression. . For system with lossy compression, quality is computed using PSNR. Mean
Squared Error is used to determine the PSNR value. Signals are dynamic in nature due to which PSNR is represented in decibels. In general, PSNR value vary between 30dB to 50dB for lossy compression provided that the bit depth of frame is 8 bits. As the bit depth of frame is increases PSNR value also increases. For example, for 12 bit it is up to 60dB and for 16 bits it is up to 80dB. For wireless transmission the acceptable PSNR value is 20dB to 25dB.

VMAF: -
Video Multi-method Assessment Fusion popularly known as VMAF is objective full reference quality matrix. Netflix created VMAF especially to have a strong correlation with subjective Mean opinion score (MOS) ratings. VMAF is used to predict subjective video quality with the help of reference and distorted video sequence which are elementary quality metrics. Each of this elementary metrics has its own strength and weakness. With respects to source. Fusion in VMAF stand for fusing this elementary metrics into final predicted metrics with the help of machine learning algorithms. Input to this algorithm is sample MOS score. This metric measures the quality loss caused by compression and rescaling.
