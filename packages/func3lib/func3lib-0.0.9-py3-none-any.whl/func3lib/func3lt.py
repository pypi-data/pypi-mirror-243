import numpy as np

# Transpose function 2D


def transpose2d(input_matrix: list[list[float]]) -> list:
    """
    The function `transpose2d` takes a 2D matrix as input and returns its transpose.

    :param input_matrix: A 2-dimensional list of floats. Each inner list represents a row in the matrix,
    and the outer list represents the entire matrix
    :type input_matrix: list[list[float]]
    :return: a transposed 2D matrix.
    """
    if not all(
        isinstance(row, list) and all(isinstance(num, (int, float)) for num in row)
        for row in input_matrix
    ):
        raise ValueError("input_matrix must be a list of lists of real numbers")
    return [list(i) for i in zip(*input_matrix)]


# Time Series Windowing function
def window1d(
    input_array, size: int, shift: int = 1, stride: int = 1
) -> list[list | np.ndarray]:
    """
    The function `window1d` takes an input array and creates overlapping windows of a specified size,
    shift, and stride.

    :param input_array: The input array is the array of values that you want to create windows from. It
    can be a list or a numpy array
    :param size: The size parameter determines the length of each window. It specifies how many elements
    from the input_array will be included in each window
    :param shift: The shift parameter determines the number of elements to shift the window by for each
    iteration. By default, it is set to 1, meaning that the window will be shifted by one element at a
    time, defaults to 1 (optional)
    :param stride: The stride parameter determines the step size between consecutive windows. It
    specifies how much the window should shift by for each iteration, defaults to 1 (optional)
    :return: The function `window1d` returns a list of 1-dimensional windows extracted from the input
    array.
    """
    if not isinstance(input_array, (list, np.ndarray)) or not np.all(
        np.isreal(input_array)
    ):
        raise ValueError("input_array must be a list or a numpy array of real numbers")
    if not all(isinstance(i, int) and i > 0 for i in [size, shift, stride]):
        raise ValueError("size, shift, and stride must be positive integers")

    windows: list[list] = []
    for i in range(0, len(input_array) - size * stride + 1, shift):
        window = input_array[i : i + size * stride : stride]
        windows.append(window)
    return windows


# Cross-Correlation function
def convolution2d(
    input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1
) -> np.ndarray:
    """
    The `convolution2d` function performs a 2D convolution operation on an input matrix using a given
    kernel and stride.

    :param input_matrix: The input_matrix is a 2D numpy array representing the input image or feature
    map on which the convolution operation will be performed. It contains the pixel values or feature
    values of the image or feature map
    :type input_matrix: np.ndarray
    :param kernel: The kernel is a 2D numpy array that represents the filter or feature detector used in
    the convolution operation. It is applied to the input_matrix to extract features or perform other
    operations. The dimensions of the kernel determine the size of the convolution window
    :type kernel: np.ndarray
    :param stride: The stride parameter determines the step size at which the kernel is applied to the
    input matrix. It specifies how much the kernel moves horizontally and vertically after each
    convolution operation. The default value is 1, which means the kernel moves one step at a time,
    defaults to 1
    :type stride: int (optional)
    :return: The function `convolution2d` returns a 2D numpy array, which is the result of applying the
    convolution operation on the input matrix using the given kernel and stride.
    """
    # Check if input_matrix and kernel are 2D numpy arrays
    if not (input_matrix.shape >= (2, 2)) or not (kernel.shape >= (2, 2)):
        ValueError("Both input_matrix and kernel should be 2D numpy arrays")

    # Check if stride is an integer and greater than 0
    if not isinstance(stride, int) or not stride > 0:
        ValueError("Stride should be an integer greater than 0")

    # Check if input_matrix is real numbers
    if not isinstance(input_matrix, np.ndarray) or not all(
        isinstance(row, list) and np.all(np.isreal(row)) for row in input_matrix
    ):
        ValueError("input_matrix should contain real numbers")

    # Check if kernel is real numbers
    if not isinstance(kernel, np.ndarray) or not all(
        isinstance(row, list) and np.all(np.isreal(row)) for row in kernel
    ):
        ValueError("kernel should contain real numbers")

    # Calculate the dimensions of the output matrix
    output_rows: int = (input_matrix.shape[0] - kernel.shape[0]) // stride + 1
    output_cols: int = (input_matrix.shape[1] - kernel.shape[1]) // stride + 1

    # Initialize the output matrix with zeros
    output_matrix = np.zeros(shape=(output_rows, output_cols))

    # Iterate over the input_matrix with the given stride, applying the kernel at each step
    for i in range(0, input_matrix.shape[0] - kernel.shape[0] + 1, stride):
        for j in range(0, input_matrix.shape[1] - kernel.shape[1] + 1, stride):
            # Calculate the sum of the element-wise multiplication of the kernel and the corresponding elements in the input_matrix
            output_matrix[i // stride, j // stride] = np.sum(
                input_matrix[i : i + kernel.shape[0], j : j + kernel.shape[1]] * kernel
            )

    return output_matrix
