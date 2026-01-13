# MSc Project – Development of a Heart Disease Prediction Mobile App

## Overview
This MSc project focuses on developing an AI-based system for predicting cardiovascular disease (CVD) and providing personalised medical advice. The work combines traditional machine learning models with Large Language Models (LLMs) and explores their integration into a mobile application.

## Problem
Cardiovascular diseases remain the leading cause of global mortality. While ML models have shown strong performance in early risk prediction, the use of LLMs for structured medical data and personalised advice is still underexplored.

## Approach
- Trained and evaluated multiple ML models on a large, balanced clinical dataset (68k+ records)
- Compared Logistic Regression, SVM, Random Forest, Neural Networks
- Fine-tuned **Llama 3.2 1B** on tabular medical data using **LoRA**
- Used **In-Context Learning (ICL)** to generate personalised, risk-aware health advice
- Designed a user-centred mobile application prototype using Kivy

## Technologies
- Python
- scikit-learn
- PyTorch
- Hugging Face Transformers
- Llama 3.2 1B
- Kivy (mobile UI)

## Results
- **Random Forest** achieved the best balanced performance (≈74% accuracy)
- Fine-tuned **Llama 3.2 1B** achieved comparable accuracy (≈73.23%)
- Demonstrated that LLMs can be effectively adapted to structured medical data
- ICL enabled coherent advice generation with explicit uncertainty handling

## Repository Notes
Due to size and computational constraints, the dataset and trained model files are not included.
All experiments can be reproduced using the provided training and evaluation scripts.

## Key Skills Demonstrated
- Machine learning model evaluation
- LLM fine-tuning with LoRA
- Working with large tabular medical datasets
- AI for healthcare
- Research-driven system design
