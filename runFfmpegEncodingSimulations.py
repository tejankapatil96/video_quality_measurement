import os
import pandas as pd
import matplotlib.pyplot as plt
import shutil

# path of executables in linux:
ffmpeg_path  = '/home/tpatil/MSProject/ffmpeg/ffmpeg-4.3.1-amd64-static/ffmpeg -y '
vmaf_exe     = '/home/tpatil/MSProject/vmaf/libvmaf/build/tools/vmafossexec '
vmaf_pickle  = ' /home/tpatil/MSProject/vmaf/model/vmaf_v0.6.1.pkl '

# global declerations:
bitrates = ['3mbps', '4mbps', '5mbps']
codeRateList = [ 'rate1', 'rate2', 'rate3', 'rate4', 'rate5', 'rate6', 'rate7', 'rate8', 'rate9', 'rate10', 'rate11' ]
rate_lists = ['4/5', '2/3', '4/7', '1/2', '4/9', '2/5', '4/11', '4/13', '2/7', '4/15', '1/4']
PER  = [0.6,	0.314,	0.136,	0.042,	0.022,	0.006,	0,	0,	0,	0,	0]
# BER  = [0.073485,	0.038275,	0.0145375,	0.005305,	0.0021075,	8.95E-04,	0,	0,	0,	0,	0]

# Added noise for each code rate as per PER:
noiseAdd = {'rate1'  : ' -bsf:v noise=10000 ',
            'rate2'  : ' -bsf:v noise=100000 ',
            'rate3'  : ' -bsf:v noise=1000000 ',
            'rate4'  : ' -bsf:v noise=10000000 ',
            'rate5'  : ' -bsf:v noise=150000000 ',
            'rate6'  : ' -bsf:v noise=2000000000 ',
            'rate7'  : '  ',
            'rate8'  : '  ' ,
            'rate9'  : '  ',
            'rate10' : '  ',
            'rate11' : '  ' }

# input clips:
clips_path = {'canal'        : ' ./source/Canal_TF1_420_8bits.yuv ',
              'finalfantasy' : ' ./source/FinalFantasy_420_1920x1080_50p.yuv ',
              'smurfs'       : ' ./source/smurfs_1920x1080_24.yuv ',
              'trail'        : ' ./source/Trail-Ends_ELD1.ts ', 
              'daVinchi'     : ' ./source/StarzDemoReel2013_DaVinchi.ts ' }

# compute the VMAF, PSNR, ISSIM scores:
def computeVmaf(bitrate, clip, codeRate):
    
    baseSettings = ' --psnr --ssim --thread 0 --susample 1 '
    vmaf_logFile = ' --log-fmt csv --log vmaf_output.csv '    
    video_size = ' yuv420p 1920 1080 '
    
    if clip != 'trail':
        original_video = clips_path[clip]
    else:
        original_video = ' inputYuv.yuv '
    
    encoded_video  = ' testOutput.yuv '
    
    compute_vmaf = vmaf_exe + video_size + original_video + ' ' + encoded_video + vmaf_pickle + vmaf_logFile + baseSettings
    print('*********************************************************************************************')
    print('compute_vmaf : ', compute_vmaf)
    print('*********************************************************************************************')
    os.system(compute_vmaf)
    
    print( 'mv vmaf_output.csv ./results/' + bitrate + '/' + clip + '/' + clip + '_' + codeRate + '.csv' )
    os.system( 'mv vmaf_output.csv ./results/' + bitrate + '/' + clip + '/' + clip + '_' + codeRate + '.csv' )    
    
    
# ffMpeg encoding:
def ffmpegEncode(bitrate, clip, codeRate):
    
    if bitrate == '3mbps':
        bitrate_enc = ' -b:v 3000000 '    
    elif bitrate == '4mbps':
        bitrate_enc = ' -b:v 4000000 '            
    elif bitrate == '5mbps':
        bitrate_enc = ' -b:v 5000000 '        
    
    drop_setting = noiseAdd[codeRate]
    print(' 1 ############ coderate is : ', codeRate, drop_setting )
        
    baseSettings = ' -c:v libx264 -profile:v high -f mpegts -muxrate 24000000 -pcr_period 30 ' + bitrate_enc + drop_setting
    
    if clip == 'trail' or clip == 'daVinchi':
        inputfile    = ' -s:v 1920x1080 -i inputYuv.yuv '        
    else:        
        inputfile    = ' -s:v 1920x1080 -i ' + clips_path[clip] + ' '
        
    outputfile   = ' temp.ts '
        
    ffmpeg_cmd = ffmpeg_path + inputfile + ' ' + baseSettings + outputfile
    print('*********************************************************************************************')
    print('ffmepg encode : ', ffmpeg_cmd)
    print('*********************************************************************************************')
    os.system( ffmpeg_cmd )
    
    
    inputfile    = ' -i temp.ts '
    outputfile   = ' testOutput.yuv '
    baseSettings = ' -threads 4 -vsync 0 -f rawvideo -pix_fmt yuv420p  '    
    ffmpeg_cmd = ffmpeg_path + inputfile + ' ' + baseSettings + outputfile
    print('*********************************************************************************************')
    print('ffmpef yuv convert : ', ffmpeg_cmd)
    print('*********************************************************************************************')
    os.system( ffmpeg_cmd )
    
    computeVmaf(bitrate, clip, codeRate)
    
    os.system( 'rm -rf testOutput.yuv temp.ts ' )


# Create teh folders to store the resutls:
def createFolders():
    
    if not os.path.exists('./results/'):
        os.makedirs( './results/')
    
    for brate in bitrates:
        
        if not os.path.exists('./results/' + brate):
            os.makedirs( './results/' + brate )
    
        for vid in clips_path.keys():
            if not os.path.exists('./results/' + brate + '/' + vid ):
                os.makedirs( './results/' + brate  + '/' + vid  )

# Main code:    
def main():
    
    createFolders()
    
    for brate in bitrates:
        for clip in clips_path.keys(): #['trail']:
            
            if clip == 'trail' or clip == 'daVinchi':
                inputfile    = ' -i ' + clips_path[clip] + ' '
                baseSettings = ' -threads 4 -vsync 0 -f rawvideo -pix_fmt yuv420p  '    
                ffmpeg_cmd = ffmpeg_path + inputfile + ' ' + baseSettings + ' inputYuv.yuv '
                print('*********************************************************************************************')
                print('ffmpef yuv convert from TS: ', ffmpeg_cmd)
                print('*********************************************************************************************')
                os.system( ffmpeg_cmd )
                        
            for cdRate in codeRateList:
                print(' 1 ############ coderate is : ', cdRate )
                ffmpegEncode(brate, clip, cdRate)
            
            os.system( 'rm -rf inputYuv.yuv ' )

# Get the results:
def getResults(vqMode):
    
    df = {'3mbps' : {}, 
          '4mbps' : {},
          '5mbps' : {} }
    
    df['3mbps'] = {'canal'       : [],
                  'finalfantasy' : [],
                  'smurfs'       : [],
                  'trail'        : [],
                  'daVinchi'     : []}
    
    df['4mbps'] = {'canal'       : [],
                  'finalfantasy' : [],
                  'smurfs'       : [],
                  'trail'        : [],
                  'daVinchi'     : [] }
    
    df['5mbps'] = {'canal'       : [],
                  'finalfantasy' : [],
                  'smurfs'       : [],
                  'trail'        : [],
                  'daVinchi'     : [] }

    
    for brate in bitrates:
        for clip in clips_path.keys():
            
            shutil.copyfile('./results/' + brate + '/' + clip + '/' + clip  + '_rate8.csv', './results/' + brate + '/' + clip + '/' + clip  + '_rate9.csv ')
            shutil.copyfile('./results/' + brate + '/' + clip + '/' + clip  + '_rate8.csv', './results/' + brate + '/' + clip + '/' + clip  + '_rate10.csv ')
            shutil.copyfile('./results/' + brate + '/' + clip + '/' + clip  + '_rate8.csv', './results/' + brate + '/' + clip + '/' + clip  + '_rate11.csv ')
            for cdRate in codeRateList:
                
                df_x = pd.read_csv( './results/' + brate + '/' + clip + '/' + clip  + '_' + cdRate + '.csv' )
                df[brate][clip].append(df_x[vqMode].mean())
    
    return df

# plot and save the end results:
def plotAndSaveResults():

    results_vmaf  = getResults('vmaf')
    results_psnr  = getResults('psnr')
    results_issim = getResults('ssim')


    for brate in bitrates:
        
        fig = plt.figure( figsize=(8, 6) )
        plt.subplot(2,1,1)
        plt.plot(rate_lists, results_vmaf[brate]['canal'], label='football', marker = 'o')
        plt.plot(rate_lists, results_vmaf[brate]['finalfantasy'], label='finalfantasy', marker = 'x')
        plt.plot(rate_lists, results_vmaf[brate]['smurfs'], label='smurfs', marker = 'd')
        plt.plot(rate_lists, results_vmaf[brate]['trail'], label='trail', marker = '*')
        plt.title('VMAF quality score vs LDPC CodeRate' + ' : encode bitrate ' + brate)
        plt.legend()
        plt.ylabel('vmaf (0-100)')
        plt.xlabel('LDPC code rates')
        plt.grid()
        
        plt.subplot(2,1,2)
        plt.plot(rate_lists, results_psnr[brate]['canal'], label='football', marker = 'o')
        plt.plot(rate_lists, results_psnr[brate]['finalfantasy'], label='finalfantasy', marker = 'x')
        plt.plot(rate_lists, results_psnr[brate]['smurfs'], label='smurfs', marker = 'd')
        plt.plot(rate_lists, results_psnr[brate]['trail'], label='trail', marker = '*')
        plt.title('PSNR quality score vs LDPC CodeRate' + ' : encode bitrate ' + brate)
        plt.legend()
        plt.ylabel('psnr')
        plt.xlabel('LDPC code rates')
        plt.grid()
        
        fig.tight_layout()
        plt.savefig( brate+'.png', bbox_inches="tight", dpi=400)


if __name__ == "__main__":
    main()
    plotAndSaveResults()
