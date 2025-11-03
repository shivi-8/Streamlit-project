# 🎲 Linear Congruential Generator (LCG) – Streamlit Simulation App

## 📘 Project Description

The **Linear Congruential Generator (LCG) Simulation App** is an interactive web-based project built using **Python** and **Streamlit** that demonstrates the working principles of pseudo-random number generation. The project aims to help learners and researchers understand how randomness is simulated computationally through simple mathematical models.

The Linear Congruential Generator is one of the oldest and most widely used algorithms for generating pseudo-random numbers. It operates based on a recurrence relation that uses four key parameters: **modulus (m)**, **multiplier (a)**, **increment (c)**, and **seed (X₀)**. The formula used is:

\[
X_{n+1} = (aX_n + c) \mod m
\]

This project implements that formula in a clean, modular Python class, ensuring reusability and logical clarity. The Streamlit interface allows users to input the parameters directly, observe the generated sequence of numbers, and visualize the effects of different parameter choices on the randomness pattern.

The user interface has been carefully designed with a **gradient background** and responsive layout to provide a modern and engaging user experience. Streamlit’s simplicity ensures that results are displayed instantly, making it easy to test and compare multiple parameter sets without writing additional code. The app also includes validation to prevent invalid inputs, ensuring stable and accurate results.

From an educational perspective, this project serves as a **visual learning tool** for students and developers interested in exploring the foundation of random number generation, simulations, and computer-based mathematical modeling. It bridges the gap between theoretical mathematics and practical implementation using an accessible and interactive platform.

The project is lightweight, runs locally via Streamlit, and requires only basic Python dependencies. Future improvements can include histogram visualization, sequence export features, and comparisons with other pseudo-random generators.

In essence, this Streamlit LCG Simulator not only illustrates the mechanics behind randomness but also showcases how **Python and Streamlit** can be combined to build powerful, interactive, and visually appealing learning tools in computational science.

---

## 🧩 Features
- Interactive input fields for all parameters  
- Real-time random number sequence generation  
- Elegant gradient UI with responsive layout  
- Built-in validation for parameters  
- Lightweight and beginner-friendly  

---

## ⚙️ Tech Stack
- **Python 3.x**
- **Streamlit**

---

## 🚀 How to Run

1. Clone this repository  
   ```bash
   git clone https://github.com/your-username/streamlit-lcg-project.git
   cd streamlit-lcg-project
