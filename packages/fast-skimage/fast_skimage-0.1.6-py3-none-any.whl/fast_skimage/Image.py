"""
Uses the scikit-image, numpy, matplotlib, PyWavelets and warnings packages to implement the Image class.
See documentation withing this class.
"""

from skimage.measure import shannon_entropy
import warnings
from skimage import color
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imsave
from skimage.morphology import disk
from skimage.filters.rank import mean
import skimage.filters.rank as skr
from numpy.fft import fft2,ifft2,fftshift,ifftshift
from skimage.restoration import estimate_sigma
from skimage.filters.rank import median
from skimage.filters import threshold_otsu
import pywt

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Image:
    """
    The Image class is designed for advanced image processing and manipulation. It includes a variety of methods to modify and analyze images.

    Written by Alexandre Le Mercier on the 21th of November 2023.
    """

    def __init__(self, path_or_ndarray):
        self.path_or_ndarray = path_or_ndarray

        if type(path_or_ndarray) == str:
            self.path = path_or_ndarray
            self.image = imread(self.path)
            self.name = self.path[:-4]
        else:
            self.image = path_or_ndarray
            self.name = "Example image"

        self.width = self.image.shape[0]
        self.height = self.image.shape[1]
        self.iscolor = (len(self.image.shape) != 2)

    def __add__(self, other):
        self.check_size(other.image)
        new_image = self.image + other.image
        new = self
        new.image = new_image
        return new

    def __sub__(self, other):
        self.check_size(other.image)
        new_image = self.image - other.image
        new = self
        new.image = new_image
        return new

    def __mul__(self, other):
        self.check_size(other.image)
        new_image = self.image * other.image
        new = self
        new.image = new_image
        return new

    def __abs__(self):
        new_image = abs(self.image)
        new = self
        new.image = new_image
        return new

    def add_watermark(self, wm, rel_x, rel_y, wm_color=BLACK, alpha=1.0, spread=1.0):
        """
        Adds watermark with more features than before.
        :param wm: numpy.ndarray (watermark) or Image
        :param rel_x: float (percentage of total width)
        :param rel_y: float (percentage of total height)
        :param wm_color: tuple (RGB tuple for color)
        :param alpha: float (transparency)
        :param spread: float (modifies the scale of the watermark along with its density)
        """
        bg_pict = self.image

        if type(wm) == Image:
            wm = wm.image

        if len(wm.shape) == 3:
            wm_width, wm_height, wm_colors = wm.shape
            bg_width, bg_height, bg_colors = bg_pict.shape
            x = rel_y * bg_width
            y = rel_x * bg_height

            # Very basic method to segment the watermark:
            wm_bg_limit = np.mean(wm)

            for pixel_color in range(3):
                for i in range(wm_width):
                    for j in range(wm_height):
                        if wm[i, j, pixel_color] >= wm_bg_limit:

                            X = int(x + i * spread)
                            Y = int(y + j * spread)

                            try:
                                bg_pict[X, Y, pixel_color] \
                                    = bg_pict[X, Y, pixel_color] * (1 - alpha) + wm_color[pixel_color] * alpha
                            except:

                                warnings.warn("Spread parameter is too large for the given image. Spread was ignored.")
                                spread = 1.0
                                X = int(x + i * spread)
                                Y = int(y + j * spread)
                                bg_pict[X, Y, pixel_color] \
                                    = bg_pict[X, Y, pixel_color] * (1 - alpha) + wm_color[pixel_color] * alpha

        else: # grayscale
            wm_width, wm_height = wm.shape
            bg_width, bg_height, bg_colors = bg_pict.shape
            x = rel_y * bg_width
            y = rel_x * bg_height

            # Very basic method to segment the watermark:
            wm_bg_limit = np.mean(wm)

            for pixel_color in range(3):
                for i in range(wm_width):
                    for j in range(wm_height):
                        if wm[i, j] >= wm_bg_limit:

                            X = int(x + i * spread)
                            Y = int(y + j * spread)

                            try:
                                bg_pict[X, Y] \
                                    = bg_pict[X, Y] * (1 - alpha) + wm_color[pixel_color] * alpha
                            except:

                                warnings.warn("Spread parameter is too large for the given image. Spread was ignored.")
                                spread = 1.0
                                X = int(x + i * spread)
                                Y = int(y + j * spread)
                                bg_pict[X, Y] \
                                    = bg_pict[X, Y] * (1 - alpha) + wm_color[pixel_color] * alpha


    def auto_enhance(self):
        """
        Automatically enhances the image by applying a series of image processing techniques
        such as histogram equalization, noise reduction, and auto-level adjustment.
        """
        if self.detect_noise():
            self.median_filter()

        self.equalize()

        self.gamma_correction(gamma=0.8)

        if len(self.image.shape) == 3:  # if not grayscale
            self.increase_saturation()

    def auto_level(self, size=5):
        """
        Applies auto-level adjustment to the image, enhancing contrast by redistributing the image intensity levels.
        :param size: int (size of the disk for local auto-level operation).
        """
        self.image = skr.autolevel(self.image, disk(size))

    def check_size(self, other_image):
        if self.image.shape != other_image.shape:
            raise AttributeError(
                f"Both images must have the same size, but image 1 has {self.image.shape} but image 2 {other_image.shape}.")

    def detect_noise(self, noisy_threshold=0.01):
        """
        Detects noise in the image by estimating the noise standard deviation across color channels.
        :param noisy_threshold: float (value from which we consider the image as noisy)
        """
        if self.iscolor:
            sigma_est = estimate_sigma(self.image, average_sigmas=True, channel_axis=-1)
        else:
            sigma_est = estimate_sigma(self.image, average_sigmas=True)

        return sigma_est > noisy_threshold

    def downsample_image(self, factor=2):
        """
        Downsamples the image by taking every nth pixel according to the factor.

        :param im: numpy.ndarray (the input image to downsample).
        :param factor: int (the downsampling factor).
        :return: numpy.ndarray (the downsampled image).
        """
        if factor < 2 or not isinstance(factor, int):
            raise ValueError(
                f"Error in Image.downsample_image: downsampling factor must be an integer greater than 1, but {factor} was given.")

        return self.image[::factor, ::factor]

    def equalize(self):
        """
         Performs histogram equalization on the image to enhance contrast. This is useful in improving the visibility
         of features in images with poor contrast.
         """
        image = self.image
        hist, _ = np.histogram(image.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * float(
            hist.max()) / cdf.max()  # Normalizes the CDF so that the highest value is scaled to the peak value of the histogram
        cdf_m = np.ma.masked_equal(cdf_normalized, 0)  # to avoid division by zero error
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')  # replace the withdrawn values
        self.image = cdf[image]

    def extract_rgb(self):
        return self.image[:, :, 0], self.image[:, :, 1], self.image[:, :, 2]

    def gamma_correction(self, gamma=1.7):
        """
        Applies gamma correction to the image. This can be used to adjust the brightness and contrast of the image.
        :param gamma: float (gamma value for the correction, higher values darken the image, lower values brighten it).
        """
        lut = np.power(np.arange(256) / 255.0, gamma) * 255
        self.image = lut[self.image.astype(np.uint8)].astype(np.uint8)

    def gray_to_color(self):
        """
        Converts a single-channel grayscale image into a 3-channel RGB image by replicating the grayscale values across the RGB channels.

        :param gray_image: numpy.ndarray
            A 2D numpy array representing the grayscale image.

        :return: numpy.ndarray
            A 3D numpy array where the grayscale values have been replicated across three channels to create an RGB image.
        """
        if len(self.image.shape) != 2:
            raise ValueError("Input image must be a 2D array representing a grayscale image.")

        # Replicate the single channel across all three RGB channels
        color_image = np.stack((self.image,) * 3, axis=-1)
        self.image = color_image

    def help(self):
        """
        Interactive help menu for the Image class that guides users to appropriate methods based on their needs.
        """
        menu = """
    Welcome to the help menu of Image. What would you like to do with your image?
        a) Segmentation
        b) Add watermark
        c) Preprocess
        d) View image
        e) Save image
    (type "exit" to leave)
        """
        print(menu)
        choice = input("Please choose an option: ").lower()
        while choice != 'exit':
            if choice == 'a':
                print(
                    "For segmentation, you can use methods like 'otsu_threshold', 'optimal_threshold', or 'texture_segmentation'.")
            elif choice == 'b':
                print("To add a watermark, use the 'add_watermark' method.")
            elif choice == 'c':
                print(
                    "For preprocessing, methods such as 'auto_enhance', 'mean_filter', and 'median_filter' are available.")
            elif choice == 'd':
                print("To view the image, use the 'show' method.")
            elif choice == 'e':
                print("To save changes to the image, use the 'save' method.")
            else:
                print("Invalid option, please try again.")

            print(menu)
            choice = input("Please choose an option: ").lower()

    def increase_saturation(self, factor=1.2):
        """
        Increases the color saturation of the image.
        :param factor: float (factor by which to increase the saturation).
        """
        hsv_image = color.rgb2hsv(self.image)
        hsv_image[:, :, 1] *= factor
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1], 0, 1)  # Ensure saturation remains in valid range
        self.image = color.hsv2rgb(hsv_image)

    def inverse(self):
        """
        Inverts the colors of the image, which can be useful for analyzing details that are hard to see in the
        original color scheme.
        """
        invert_lut = np.array([255 - i for i in range(256)])
        self.image = invert_lut[self.image]


    def mean_filter(self, size=2):
        """
        Applies a mean filter to the image, which is useful for noise reduction and smoothing.
        If the image is in color, the filter is applied to each channel separately.
        :param size: int (size of the mean filter kernel).
        """
        if not self.iscolor:
            self.image = mean(self.image, disk(size))
        else:
            for i in range(3):  # Assuming the image has 3 channels (RGB)
                self.image[:, :, i] = mean(self.image[:, :, i], disk(size))

    def median_filter(self, size=2):
        """
        Applies a median filter to the image, effective in reducing salt-and-pepper noise while preserving edges.
        If the image is in color, the filter is applied to each channel separately.
        :param size: int (size of the median filter kernel).
        """
        if not self.iscolor:
            self.image = median(self.image, disk(size))
        else:
            for i in range(3):  # Assuming the image has 3 channels (RGB)
                self.image[:, :, i] = median(self.image[:, :, i], disk(size))

    def optimal_threshold(self, initial_threshold=128, tolerance=1):
        """
        Find the threshold for an image using an iterative algorithm.

        :param initial_threshold: float, the initial guess for the threshold
        :param tolerance: float, the convergence tolerance
        :return: float, the found threshold
        """
        T = initial_threshold
        while True:
            # Step 2: Divide pixels into two groups based on the threshold
            G1 = self.image[self.image > T]
            G2 = self.image[self.image <= T]

            # Step 3: Compute mean (centroid) of each group
            m1 = np.mean(G1) if len(G1) > 0 else 0
            m2 = np.mean(G2) if len(G2) > 0 else 0

            # Step 4: Compute new threshold
            T_new = (m1 + m2) / 2

            threshold_lut = np.array([i if i >= T else 0 for i in range(256)])
            self.image = threshold_lut[self.image]

            # Check for convergence
            if np.abs(T - T_new) < tolerance:
                break
            T = T_new

    def otsu_threshold(self):
        """
        Applies Otsu's thresholding to the image to convert it to a binary image where the threshold is determined automatically.
        """
        th = threshold_otsu(self.image)
        self.image = self.image > th

    def reduce(self, reduction_factor=2):
        """
        Reduces the number of gray levels in the image, which can be useful for reducing image size and
        emphasizing certain features.
        :param reduction_factor: int (factor by which to reduce the gray levels).
        """
        reduced_lut = np.array([i // reduction_factor for i in range(256)])
        self.image = reduced_lut[self.image]

    def reduce_dithering(self, fourier_filter_radius=20):
        """
        Reduces dithering noise in the image by applying a Fourier transform-based filter. This is useful for
        cleaning up images with dithering artifacts.
        :param fourier_filter_radius: int (radius for the Fourier filter).
        """
        f = fftshift(fft2(self.image))  # shift Fourier image so that the center corresponds to low frequencies
        for x in range(len(f)):
            for y in range(len(f[x])):
                f[x, y] = f[x, y] * self.round_mask(x, y, fourier_filter_radius, center=True)

        self.fourier_amplitute = np.sqrt(np.real(f) ** 2 + np.imag(f) ** 2)
        self.image = ifft2(ifftshift(f)).real

    def reset(self):
        """
        Resets the image to its original state.
        """
        try:
            self.name = self.path[0:-4]
        except:
            Warning("Cannot reset the name")
        self.image = imread(self.path_or_ndarray)

    def round_mask(self, x, y, radius_lim, center=False):
        if center:
            x0, y0 = self.image.shape[0] // 2, self.image.shape[1] // 2
        else:
            x0, y0 = 0, 0

        x, y = x - x0, y - y0
        radius = np.sqrt(x ** 2 + y ** 2)
        return int((radius <= radius_lim))


    def save(self):
        """
        Saves the updated image file.
        """
        imsave(self.name, self.image)

    def save_image_data(self, filename):
        """
        Saves the np.ndarray of the image in an external text file in Python list format.
        :param image: np.ndarray of the image data
        :param filename: The name of the file where to save the data
        """
        with open(filename, 'w', encoding='utf-8') as file:
            image_list = self.image.tolist()
            file.write(str(image_list))


    def show(self, size=6, title='', x_axis='', y_axis='', type_of_plot='rgb', subplots=(0, 0, 0), greyscale=False,
             normalize=False, axis=False, threshold=None, colorbar=False):
        """
        Shortcut function to execute commands often used to plot functions and show images.
        :param size: int if square or bool if rectangle
        :param title: str
        :param x_axis: str
        :param y_axis: str
        :param type_of_plot: 'rgb' for showing the rgb image, 'hist' for histograms
        :param subplots: tuple (a, b, c) for matplotlib's subplots
        :param greyscale: bool
        :param normalize: bool  (for histograms only)
        :param threshold: float (draws a red line in the histogram)
        :return: shows the plot (no return value).
        """

        image = self.image
        if len(image) == 3:
            self.iscolor = True
        else:
            self.iscolor = False

        if len(subplots) != 3 and subplots != (0, 0, 0):
            raise AttributeError("'subplots' must contain 3 values")

        if subplots[2] == (1 or 0):
            if type(size) == int:
                plt.figure(figsize=(size, size))
            elif type(size) == tuple:
                plt.figure(figsize=size)
            else:
                raise AttributeError("'Size' must be either an integer or a tuple")

        if subplots != (0, 0, 0):
            a, b, c = subplots
            plt.subplot(a, b, c)
        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)

        if type_of_plot == 'rgb':
            if title == '':
                plt.title(self.name)
            if not self.iscolor:
                plt.imshow(image, cmap='gray')
            elif greyscale:
                image = color.rgb2gray(image)
                self.iscolor = False
                plt.imshow(image, cmap='gray')
            else:
                plt.imshow(image)
        elif type_of_plot == 'hist':
            if not self.iscolor:
                if title == '':
                    plt.title("Histogram of greyscale intensities")
                hist, _ = np.histogram(image, bins=256, range=(0, 255))
                if normalize:
                    hist /= hist.sum()
                plt.plot(hist)
                if threshold != None:
                    plt.plot([threshold, threshold], [0, hist.max()], 'r-')
            else:
                if title == '':
                    plt.title("Histogram of RGB values")
                r, g, b = self.extract_rgb()
                r = r.flatten()
                g = g.flatten()
                b = b.flatten()
                rhist, _ = np.histogram(r, bins=256, range=(0, 255))
                ghist, _ = np.histogram(g, bins=256, range=(0, 255))
                bhist, _ = np.histogram(b, bins=256, range=(0, 255))
                if normalize:
                    rhist = rhist / np.sum(rhist)
                    ghist = ghist / np.sum(ghist)
                    bhist = bhist / np.sum(bhist)
                plt.plot(rhist, color='red', label='Red')
                plt.plot(ghist, color='green', label='Green')
                plt.plot(bhist, color='blue', label='Blue')
                plt.legend()
                if threshold != None:
                    plt.plot([threshold, threshold], [0, rhist.max()], 'r-')
        else:
            raise AttributeError("'type_of_plot' must be either 'rgb' or 'hist'.")

        if not axis:
            plt.axis('off')

        if colorbar:
            plt.colorbar()

        if subplots[2] == subplots[0] * subplots[1]:
            plt.show()

    def sliding_window(self, PATCH_SIZE, method='max', return_mask=False):
        """
        Applies a sliding window technique over the image to compute a texture descriptor for each window.

        The function moves the patch across the image and computes the descriptor defined by the 'method' parameter for each position.

        :param PATCH_SIZE: A tuple of two integers (height, width) specifying the size of the patch for the sliding window.
        :param method: A string specifying the method of texture descriptor calculation. Accepted values are 'max' or 'entropy'.
        :param return_mask: True if the user only wants to extract the mask
        :return: The mask if "return_mask" is set on "True" or nothing otherwise (directly modifies the image)
        :raises AttributeError: If an invalid method argument is passed.
        """
        im = self.image
        output = np.zeros((im.shape[0], im.shape[1]))
        for i in range(0, im.shape[0] - PATCH_SIZE[0] + 1, PATCH_SIZE[0]):
            for j in range(0, im.shape[1] - PATCH_SIZE[1] + 1, PATCH_SIZE[1]):
                patch = im[i:i + PATCH_SIZE[0], j:j + PATCH_SIZE[1]]
                if method == 'max':
                    output[i:i + PATCH_SIZE[0], j:j + PATCH_SIZE[1]] = self.texture_descriptor_max(patch)
                elif method == 'entropy':
                    output[i:i + PATCH_SIZE[0], j:j + PATCH_SIZE[1]] = self.texture_descriptor_entropy()
                else:
                    return AttributeError(
                        f"Error in Image.sliding_windows: method argument should be 'max' or 'entropy' but {method} was given.")

        if return_mask:
            return Image(output)
        else:
            self.image = output

    def stretch(self, T_min, T_max):
        """
        Stretches the histogram of the image between specified minimum and maximum values, which enhances the
        contrast in a specific intensity range.
        :param T_min: int (minimum threshold for stretching).
        :param T_max: int (maximum threshold for stretching).
        """
        stretched_lut = np.array(
            [0 if i < T_min else 255 if i > T_max else ((i - T_min) / (T_max - T_min)) * 255 for i in range(256)])
        self.image = stretched_lut[self.image]

    def texture_descriptor_entropy(self):
        """
        Computes the Shannon entropy of the image as a texture descriptor.
        Entropy measures the randomness in the image which can be used as a proxy for texture complexity.

        :return float: The entropy of the image.
        """
        return shannon_entropy(self)

    def texture_descriptor_max(self, patch):
        """
        Computes the maximum value in a given patch of the image as a texture descriptor.
        This simple approach captures the highest intensity present in the patch.

        :param patch (numpy.ndarray): The image patch for which to compute the maximum value descriptor.

        :return:  float: The maximum value in the patch.
        """
        e = patch.max()
        return e

    def texture_segmentation(self, patch_size=(3, 3), method='max'):
        """
        Segments the image based on texture using a specified texture descriptor and segmentation method.

        :param patch_size: (tuple of int): The size of the patches to be used for texture descriptor computation.
        :param method (str): The method used for texture descriptor calculation, 'max' for maximum value or 'entropy'.
        """
        if type(patch_size) == int:
            patch_size = (patch_size, patch_size)

        self.sliding_window(patch_size, method=method)
        self.otsu_threshold()
        self.iscolor = False

    def threshold(self, threshold):
        """
         Applies thresholding to the image, setting all pixels below the threshold to zero. This is useful for
         segmenting or emphasizing certain features in the image.
         :param threshold: int (threshold value).
         """
        threshold_lut = np.array([i if i >= threshold else 0 for i in range(256)])
        self.image = threshold_lut[self.image]
