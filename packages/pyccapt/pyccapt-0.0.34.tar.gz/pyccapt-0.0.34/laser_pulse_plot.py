import numpy as np
import matplotlib.pyplot as plt





def different_amplitudes(max_amplitude = 0.95, min_amplitude = 0.69):
	# Parameters for the sinusoidal curve
	frequency = 0.6  # Frequency of the sinusoid
	num_points = 1000  # Number of points for the curve
	x = np.linspace(-20, 20, num_points)

	# Parameters for the Gaussian envelope
	mu = 0.0  # Mean of the Gaussian
	sigma = 3.0  # Standard deviation of the Gaussian
	gaussian_envelope_1 = np.exp(-0.5 * ((x - mu) / sigma) ** 2)
	gaussian_envelope_2 = np.exp(-0.5 * ((x - mu) / sigma) ** 2) * -1

	# Generate and save images for each amplitude
	for amplitude in np.linspace(max_amplitude, min_amplitude, 20):
		# Generate the sinusoidal curve
		sinusoid = amplitude * np.sin(2 * np.pi * frequency * x)

		# Multiply the sinusoidal curve by the Gaussian envelope
		sinusoidal_with_envelope = sinusoid * gaussian_envelope_1

		gaussian_envelope_1 = gaussian_envelope_1 * amplitude
		gaussian_envelope_2 = gaussian_envelope_2 * amplitude
		# Plot the figure
		plt.figure(figsize=(8, 6))
		plt.plot(x, sinusoidal_with_envelope, color='blue', linewidth=2)
		plt.plot(x, gaussian_envelope_1, color='blue', linewidth=1, linestyle='--')
		plt.plot(x, gaussian_envelope_2, color='blue', linewidth=1, linestyle='--')

		plt.xlabel("Time (fs)", fontsize=20)
		plt.ylabel("Electric field (a. u.)", fontsize=20)
		# Increase the size of numbers on x and y axes
		plt.xticks(fontsize=16)
		plt.yticks(fontsize=16)
		# Adjust the spacing to prevent labels from going out of bounds
		plt.subplots_adjust(bottom=0.15, left=0.15)

		# Set the range for x and y axes
		plt.xlim(-20, 20)  # Set the x-axis range from 0 to 10
		plt.ylim(-1, 1)  # Set the y-axis range from -3 to 3

		# Save the figure
		image_filename = f"amplitude_{amplitude:.2f}.png"
		plt.savefig(image_filename)

		plt.close()

def different_pulse_width(sigma_min=0.5, sigma_max=5.0):
	# Parameters for the sinusoidal curve
	frequency = 0.6  # Frequency of the sinusoid
	num_points = 1000  # Number of points for the curve
	x = np.linspace(-20, 20, num_points)

	max_amplitude = 0.95
	min_amplitude = 0.4
	amplitude_array = np.linspace(max_amplitude, min_amplitude, 10)
	# Generate and save images for each amplitude
	for i, pulse_width in enumerate(np.linspace(sigma_min, sigma_max, 10)):
		# Parameters for the Gaussian envelope
		mu = 0.0  # Mean of the Gaussian
		sigma = pulse_width  # Standard deviation of the Gaussian
		gaussian_envelope_1 = np.exp(-0.5 * ((x - mu) / sigma) ** 2)
		gaussian_envelope_2 = np.exp(-0.5 * ((x - mu) / sigma) ** 2) * -1

		amplitude = amplitude_array[i]
		# Generate the sinusoidal curve
		sinusoid = amplitude * np.sin(2 * np.pi * frequency * x)

		# Multiply the sinusoidal curve by the Gaussian envelope
		sinusoidal_with_envelope = sinusoid * gaussian_envelope_1

		gaussian_envelope_1 = gaussian_envelope_1 * amplitude
		gaussian_envelope_2 = gaussian_envelope_2 * amplitude
		# Plot the figure
		plt.figure(figsize=(8, 6))
		plt.plot(x, sinusoidal_with_envelope, color='blue', linewidth=2)
		plt.plot(x, gaussian_envelope_1, color='blue', linewidth=1, linestyle='--')
		plt.plot(x, gaussian_envelope_2, color='blue', linewidth=1, linestyle='--')

		plt.xlabel("Time", fontsize=20)
		plt.ylabel("Pulse energy", fontsize=20)
		# Increase the size of numbers on x and y axes
		plt.xticks(fontsize=16)
		plt.yticks(fontsize=16)
		# Adjust the spacing to prevent labels from going out of bounds
		plt.subplots_adjust(bottom=0.15, left=0.15)

		# Set the range for x and y axes
		plt.xlim(-20, 20)  # Set the x-axis range from 0 to 10
		plt.ylim(-1, 1)  # Set the y-axis range from -3 to 3

		# Save the figure
		image_filename = f"pulse_width_{pulse_width:.2f}.png"
		plt.savefig(image_filename)

		plt.close()

different_pulse_width()
print("Images saved for different amplitudes.")
