def input_pipeline( image ):
    img = np.copy( image )
    img = undistort_image( img );
    
    #Converting to HLS
    hls = cv2.cvtColor( img, cv2.COLOR_RGB2HLS ).astype(np.float)
    
    h_channel = hls[:,:,0]
    l_channel = hls[:,:,1]
    s_channel = hls[:,:,2]
        
    #Extracting white portions of the image
    l_binary = np.zeros_like( l_channel )
    l_binary[ ( l_channel > 220 ) & (l_channel <= 255 )] = 1
    
    #bin_rgb_w = apply_bin_threshold( l_channel )
    #mag_rgb_w = mag_thresh( l_binary, sobel_kernel=15, mag_thresh=( 190, 255 ) )    
    #dir_rgb_w = dir_threshold( l_binary, sobel_kernel=15, thresh=( 0.7, 1.3 ) )
    #binary_white = np.zeros_like( dir_rgb_w )
    #binary_white[ ( ( mag_rgb_w == 1 ) & ( dir_rgb_w == 1 ) ) ] = 1
    
    #Based on: https://medium.com/@tjosh.owoyemi/finding-lane-lines-with-colour-thresholds-beb542e0d839
    #It's yellow extraction seems to work pretty good
    
    #Extracting yellow portions of the line
    lower = np.array([20,  120,  80],dtype="uint8")
    upper = np.array([45, 200, 255],dtype="uint8")
    
    mask = cv2.inRange( hls, lower, upper )
    hls_y = cv2.bitwise_and( image, image, mask=mask).astype( np.uint8 )
    hls_y = cv2.cvtColor( hls_y, cv2.COLOR_HLS2RGB )
    hls_y = cv2.cvtColor( hls_y, cv2.COLOR_RGB2GRAY )
    
    #sobelx_hls_y = mag_thresh( hls_y, orient='x', thresh=(20,120) )
    bin_hl_y = apply_bin_threshold( hls_y )
    
    #mag_hls_y = mag_thresh( hls_y, sobel_kernel=15, mag_thresh=( 190, 255 ) )
    #dir_hls_y = dir_threshold( hls_y, sobel_kernel=15, thresh=( 0.7, 1.3 ) )   
    #combine_hls_y = np.zeros_like( dir_hls_y )
    #combine_hls_y[ ( mag_hls_y == 1 ) & ( dir_hls_y == 1 ) ] = 1
        
    combined = np.zeros_like( bin_hl_y )    
    combined[ ( ( bin_hl_y == 1 ) | ( l_binary == 1 ) ) ] = 1   

    return(  np.uint8( combined*255 ) )


def apply_bin_threshold( img, bin_threshold=( 20, 255 ) ):
    bin_img = np.zeros_like( img )
    bin_img[ ( img >= bin_threshold[0] ) & ( img <= bin_threshold[1] ) ] = 1
    
    return bin_img