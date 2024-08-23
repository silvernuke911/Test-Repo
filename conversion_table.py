import numpy as np 
import matplotlib.pyplot as plt

dlat = 1
start_lat = -85
end_lat = 85
lat = np.arange(start_lat, end_lat+dlat, dlat)
print(lat)

# def mercator_conversion(latlist):
#     rad_list = rad_list = np.deg2rad(latlist)
#     conv_list = np.log(np.tan(rad_list)+ (1 / np.cos(rad_list)))-np.log(np.tan(rad_list - dlat_list)+ (1 / np.cos(rad_list - dlat_list)))
#     return conv_list

def numerical_differentiator(x, func):
    """
    Returns the array of the numerical derivative of a function f(x), dy/dx.
    
    Parameters:
        x (np.ndarray): Array of numbers representing values on the x axis.
        func (callable): A function taking x as an input.
    
    Returns:
        np.ndarray: Array of numerical derivative values.
    """
    y = func(x)  # Creating the function values
    output = np.zeros_like(y)  # Initializing an array
    
    # Calculate differences for the interior points using central difference
    dx = np.diff(x)
    dy = np.diff(y)
    output[1:-1] = (y[2:] - y[:-2]) / (x[2:] - x[:-2])
    
    # Forward difference for the first point
    output[0] = (y[1] - y[0]) / dx[0]
    
    # Backward difference for the last point
    output[-1] = (y[-1] - y[-2]) / dx[-1]
    
    return output

def mercator_function(lat):
    rad_lat = np.deg2rad(lat)
    return np.log(np.tan(rad_lat) + (1 / np.cos(rad_lat)))

def mercator_conversion(latlist):
    # Convert the latitude list to a NumPy array
    lat_list = np.array(latlist)
    conv_list = np.rad2deg(numerical_differentiator(lat_list,mercator_function))
    # print(conv_list)
    # rad_lat = np.deg2rad(lat_list)
    # conv_list = np.log(np.tan(rad_lat) + (1 / np.cos(rad_lat))) #- np.log(np.tan(rad_lat-dlat) + (1 / np.cos(rad_lat-dlat)))
    return conv_list

conversion_list = mercator_conversion(lat)
print(lat)
print(conversion_list)

plt.plot(lat, mercator_function(lat))
plt.ylim([-3,3])
plt.show()

plt.plot(lat, conversion_list)
plt.ylim([0,5])
plt.show()
