import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def generate_input_signal(signal_type, t, amplitude, frequency, duty_cycle):
    if signal_type == 'Step Function':
        return np.ones_like(t)
    elif signal_type == 'Sinusoidal Function':
        return amplitude * np.sin(2 * np.pi * frequency * t)
    elif signal_type == 'Square Wave':
        return amplitude * (np.sign(np.sin(2 * np.pi * frequency * t)) + 1) / 2

def second_order_lag(input_signal, damping_ratio, natural_frequency, lower_saturation_limit, upper_saturation_limit):
    output_signal = np.zeros_like(input_signal)
    state = 0

    for i in range(1, len(input_signal)):
        delta_t = input_signal[i] - input_signal[i-1]
        state += (delta_t - 2 * damping_ratio * natural_frequency * state) / (1 + 2 * damping_ratio * natural_frequency)

        # Apply saturation to the state
        state = np.clip(state, lower_saturation_limit, upper_saturation_limit)

        output_signal[i] = state

    return output_signal

def main():
    st.set_page_config(layout="wide")
    st.title('Second-Order Lag System with Saturation')

    # Sidebar for system parameters
    st.sidebar.header('System Parameters')
    damping_ratio = st.sidebar.slider('Damping Ratio', 0.1, 2.0, 0.7, step=0.1)
    natural_frequency = st.sidebar.slider('Natural Frequency', 0.01, 5.0, 0.1, step=0.01)
    
    # Sliders for lower and upper saturation limits
    lower_saturation_limit = st.sidebar.slider('Lower Saturation Limit', -2.0, 2.0, -0.1, step=0.01)
    upper_saturation_limit = st.sidebar.slider('Upper Saturation Limit', -2.0, 2.0, 0.1, step=0.01)

    # Sidebar for input signal parameters
    st.sidebar.header('Input Signal Parameters')
    signal_type = st.sidebar.selectbox('Select Input Signal', ['Sinusoidal Function', 'Square Wave', 'Step Function'])

    if signal_type == 'Sinusoidal Function':
        amplitude = st.sidebar.slider('Sinusoidal Amplitude', 0.1, 10.0, 1.0, step=0.1)
        frequency = st.sidebar.slider('Sinusoidal Frequency', 0.1, 10.0, 1.0, step=0.1)
        duty_cycle = None
    elif signal_type == 'Square Wave':
        amplitude = st.sidebar.slider('Square Wave Amplitude', 0.1, 2.0, 1.0, step=0.1)
        frequency = st.sidebar.slider('Square Wave Frequency', 0.1, 10.0, 1.0, step=0.1)
        duty_cycle = st.sidebar.slider('Square Wave Duty Cycle', 0.1, 0.9, 0.5, step=0.1)
    else:
        amplitude, frequency, duty_cycle = None, None, None

    # Generate time vector
    t = np.linspace(0, 5, 1000)

    # Generate input signal
    input_signal = generate_input_signal(signal_type, t, amplitude, frequency, duty_cycle)

    # Apply second-order lag with saturation
    output_signal = second_order_lag(input_signal, damping_ratio, natural_frequency, lower_saturation_limit, upper_saturation_limit)

    # Plot the input and output signals on the same graph
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t, input_signal, label='Input Signal')
    ax.plot(t, output_signal, label='Output Signal with Saturation')
    ax.set_title('Second-Order Lag System with Saturation for Smoothing')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.legend()
    st.pyplot(fig)

if __name__ == '__main__':
    main()
