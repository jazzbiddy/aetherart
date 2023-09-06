from PIL import Image
import requests
import pygame

import sys
import time
import json
import os
import socket


### USER SETTINGS

# Display Information
screen_number = 1
# SlideShow Information
refresh_interval = 5
categories = 'turtles, cats, dogs'
orientation = 1
content_filter = 1
frame_number = 1
# API Account Information
api_key = ''



### PRE SETTINGS INTERNAL VARIABLES

has_api_key = False
invalid_api_key = False
has_ip_address = False
has_photo = False
has_merged_image = False
has_swapped_screen = False
api_url = 'https://api.unsplash.com/photos/random?'
frame_path = ''


def load_settings():
    
    
    global screen_number
    global refresh_interval
    global categories
    global orientation
    global content_filter
    global frame_number
    global api_key
    global has_api_key

    
    # Load settings from settings.json
    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)

    # Extract variables from the settings
    screen_number = settings.get('screen_number', screen_number) - 1
    refresh_interval = settings.get('refresh_interval', refresh_interval) * 60
    categories = settings.get('categories', categories)
    orientation = settings.get('orientation', orientation)
    content_filter = settings.get('content_filter', content_filter)
    frame_number = settings.get('frame_number', frame_number) - 1
    api_key = settings.get('api_key', api_key)

    if (api_key != ''):
        has_api_key = True


    print ('Loaded the following Settings:')
    print ('screen_number: ' + str(screen_number))
    print ('refresh_interval: ' + str(refresh_interval))
    print ('categories: ' + str(categories))
    print ('orientation: ' + str(orientation))
    print ('content_filter: ' + str(content_filter))
    print ('frame_number: ' + str(frame_number))
    print ('api_key: ' + str(api_key))
    print ('Has API Key: ' + str(has_api_key))

# load settings
load_settings()    

def getFrameFileName(frame_index):
    
    global frame_path

    frame_dir = 'frames/'

    # Ensure the directory exists
    if not os.path.exists(frame_dir):
        raise ValueError("Frames Directory does not exist.")

    # Get a list of all files in the directory
    all_files = os.listdir(frame_dir)

    # Check if the index is within the valid range
    if frame_index < 0 or frame_index >= len(all_files):
        raise ValueError("Frame Index is out of range.")

    # Return the file path corresponding to the index
    return all_files[frame_index]

def getLocalIPAddress():
    global has_ip_address
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to a remote server (doesn't actually send data)
        s.connect(("8.8.8.8", 80))  # Using Google's public DNS server

        # Get the local IP address
        ip_address = s.getsockname()[0]

        # Close the socket
        s.close()

        has_ip_address = True

        return ip_address
        
    except Exception as e:
        return str(e)

def get_resolution():
    pygame.init()
    # num_screens = pygame.display.get_num_displays()
    # print ('Number of screens: ' + str(num_screens))

    resolution = None
    pygame.init()
    screen = pygame.display.set_mode()  # Create a minimal window
    info = pygame.display.Info()
    pygame.quit()

    resolution = (info.current_w, info.current_h)
    return resolution



### POST SETTINGS INTERNAL VARIABLES

# Image request headers
headers = {'Authorization': 'Client-ID ' + api_key}

screen_info = get_resolution()
screen_width = screen_info[0]
screen_height = screen_info[1]
print ('Screen Width: ' + str(screen_width))
print ('Screen Height: ' + str(screen_height))

# photo refresh timers
#image_change_time = time.time() + refresh_interval
image_change_time = 0

# force load: 
# When the settings are updated from the web page, a file is written
# to trigger the reloading of settings. 
force_load_last_check_time = 0
force_load_check_interval = 10  # this will check for the presence of the force load file every N seconds

# slideshow settings
slideshow_running = True
merged_image = None # variable to hold the merged image
frame_image_path = 'frames/' + str(getFrameFileName(frame_number))
downloaded_image_path = 'images/image.jpg'

# Frame dimensions
frame_default_width = 3840
frame_default_height = 2160
# Photo dimensions
photo_default_width = 3240
photo_default_height = 1560

system_ip_address = getLocalIPAddress()
print ('Pi IP Addr: ' + str(system_ip_address))




def get_new_photo():
    global has_photo
    global invalid_api_key

    has_error = False


    load_settings()

    has_photo = False

    if orientation == 1:
        display_orienation = 'landscape'
    else:
        display_orienation = 'portait'
    
    if content_filter == 1:
        photo_content = 'high'
    else:
        photo_content = 'low'

        
    api_address = api_url + 'orientation=' + display_orienation + '&content_filter=' + photo_content + '&query=' + categories.strip()
    print (api_address)

    api_address = api_address.strip()
    print (headers)
    
    try:
        json_response = requests.get(api_address, headers=headers,)

        print (json_response)
    except:
        print ("json request has error!")
        has_error = True
        

    if (not has_error):

        if json_response.status_code == 200:
            # Parse the JSON response
            data = json_response.json()
            # print (data)
            
            # Access the 'urls' dictionary and then the 'full' field
            photo_url = data['urls']['full']
            
            # print("Photo URL:", photo_url)
            

            # now get the photo from it's url
            try:
                photo_response = requests.get(photo_url, headers=headers)
            except:
                 has_error = True

            if (not has_error):
            
   
                # Check if the request was successful (status code 200)
                if photo_response.status_code == 200:
                    # Get the content (binary data) from the response
                    image_data = photo_response.content
                                
                    # print (f"Image downloaded and stored to memory")

                    # Specify the local file path where you want to save the image
                    local_file_path = "images/image.jpg" 
                    
                    # Write the image content to the local file
                    with open(local_file_path, "wb") as file:
                        file.write(image_data)
                    
                    has_photo = True
                    
                    # print(f"Image downloaded and saved to {local_file_path}")
                else:
                    print(" GET PHOTO Error:", photo_response.status_code)
            else:
                print("Error getting Image. Using old image")

            
        elif json_response.status_code == 401:
            invalid_api_key = True
            
        else:
            print("GET JSON Error:", json_response.status_code)
    else:
        print("Error getting JSON.")

def merge_photo_and_frame():
    global merged_image
    global has_merged_image
    global has_swapped_screen

    print('Picture Frame Path: ' + str(frame_image_path))

    # Get the frame
    picture_frame = Image.open(frame_image_path)
    frame_original_width, frame_original_height = picture_frame.size

    # print('frame_orig_size: ' + str(picture_frame.size))
    # print('screen size: (' + str(screen_width) + ', ' + str(screen_height) + ')')

    if (screen_width != frame_original_width or screen_height != frame_original_height):
        picture_frame = picture_frame.resize((screen_width, screen_height))

    # get new size
    frame_new_width, frame_new_height = picture_frame.size

    # Calculate the scaling factor for resizing Image1
    scale_factor_width = frame_new_width / frame_original_width
    scale_factor_height = frame_new_height / frame_original_height
    
    # Ensure image is in RGBA mode (for compatibility)
    picture_frame = picture_frame.convert('RGBA')


    

    # Get downloaded image
    downloaded_image = Image.open(downloaded_image_path)

    # Resize to proper starting size
    downloaded_image = downloaded_image.resize((photo_default_width, photo_default_height))

    dload_image_width, dload_image_height = downloaded_image.size

    # Calculate the scaled dimensions of Image2
    dload_image_new_width = int(dload_image_width * scale_factor_width)
    dload_image_new_height = int(dload_image_height * scale_factor_height)

    # Resize Image2 while maintaining the aspect ratio
    downloaded_image = downloaded_image.resize((dload_image_new_width, dload_image_new_height))

       # Calculate the offsets to center Image2 within the resized Image1
    x_offset = (screen_width - dload_image_new_width) // 2
    y_offset = (screen_height - dload_image_new_height) // 2


        
    # # downloaded_image = downloaded_image.resize((2928, 1484))
    # downloaded_image = downloaded_image.resize((screen_width, screen_height))

    # Create a new blank image with the desired dimensions (3840x2160)
    merged_image = Image.new('RGBA', (screen_width, screen_height), (0, 0, 0, 0))

    # # Calculate the position to center the background image
    # x_offset = (merged_image.width - downloaded_image.width) // 2
    # y_offset = (merged_image.height - downloaded_image.height) // 2

    # Paste the centered background image onto the merged image
    merged_image.paste(downloaded_image, (x_offset, y_offset))
    # Ensure image is in RGB mode (for compatibility)
    merged_image = merged_image.convert('RGB')

    
    # Paste the top image onto the background image
    merged_image.paste(picture_frame, (0, 0), picture_frame)

    
    # # Save the merged image
    # merged_image.save('merged_image.jpg')

    # # Close the image files
    downloaded_image.close()
    picture_frame.close()

    has_merged_image = True
    has_swapped_screen = False

def check_reload_flag():
    global image_change_time
    # Check for the exit signal flag file
    if os.path.exists('reload_flag.txt'):
        os.remove('reload_flag.txt')
        print ("reload flag found!")
        
        # reload settings
        load_settings()
        image_change_time = 0



# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((screen_width, screen_height))
#screen = pygame.display.set_mode()

#hide mouse cursor
pygame.mouse.set_visible(False)


# Error Screen
def show_error_screen(error_type):

    if error_type == 1:
        screen_msg1 = "Missing Photos API Key"
        screen_msg2 = "Open configuration webpage at http://" + str(system_ip_address) 
        screen_msg3 = ""  
        
    elif error_type == 2:
        screen_msg1 = "Invalid Photos API Key"
        screen_msg2 = "Error using provided key"
        screen_msg3 = "Use configuration webpage at http://" + str(system_ip_address) + " to fix."
    
    elif error_type == 3:
        screen_msg1 = "Issue Getting Photo"
        screen_msg2 = "There was an unknown error :( "
        screen_msg3 = "Check configuration webpage at http://" + str(system_ip_address) + " to fix."
    
    else:
        screen_msg1 = "Unknown Error"
        screen_msg2 = "Who knows. Check your setup?"
        screen_msg3 = "Configuration webpage located at http://" + str(system_ip_address)


    background_color = (255, 0, 0)  # Red color in RGB

    font1 = pygame.font.Font(None, 48)  # None specifies the default font
    font2 = pygame.font.Font(None, 36)  # None specifies the default font

    text_surface1 = font1.render(screen_msg1, True, (255, 255, 255))  # White text color
    text_surface2 = font2.render(screen_msg2, True, (255, 255, 255))  # White text color
    text_surface3 = font2.render(screen_msg3, True, (255, 255, 255))  # White text color

    screen.fill(background_color)
    screen.blit(text_surface1, (25, 25))  # Position the text surface
    screen.blit(text_surface2, (25, 65))  # Position the text surface
    screen.blit(text_surface3, (25, 95))  # Position the text surface

    pygame.display.flip()



# Main loop
while slideshow_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            slideshow_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Check if the 'p' key is pressed. if it is - quit
                slideshow_running = False           

    
    currentTime = time.time()

    # force load check
    if currentTime >= force_load_check_interval:
        check_reload_flag()
        force_load_last_check_time = currentTime + force_load_check_interval


    if not has_api_key:
        show_error_screen(1)
    else:
        # normal slide show image change check
        if currentTime >= image_change_time:  
            print('----------')
            print ('TIME: ' + str(currentTime))
            print ('IMG CHNG TIME: ' + str(image_change_time))          

            print ('Getting New Photo')
            get_new_photo()
        
            if not has_photo:
                if invalid_api_key:
                    show_error_screen(2)
                else:
                   show_error_screen(3) 
                   
            else:
                print ('Success Downloading Photo')
                print('----------')
                print ('Merging photo with frame')
                merge_photo_and_frame()

            # Update the timer for the next image change
            image_change_time = currentTime + refresh_interval


        if has_merged_image and not has_swapped_screen:
            print ('Updating Pygame with merged image')

                # Convert the merged image to a format compatible with pygame
            pygame_image = pygame.image.fromstring(merged_image.tobytes(), merged_image.size, merged_image.mode)

            # Blit (draw) the image onto the screen
            screen.blit(pygame_image, (0, 0))

            # Update the display
            pygame.display.flip()

            has_swapped_screen = True

        


### Slideshow is no longer running. quit pygame and this script    

# Quit pygame
pygame.quit()

# Exit the script
sys.exit()



