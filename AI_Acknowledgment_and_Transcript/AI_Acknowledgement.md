# AI Acknowledgement

**DAAW citation for AI assistance — MA289 Competition 2 (Spoken Digit Classification, 6 vs 7)**

<!-- One sentence per line for easy reading in the editor; Markdown renders it as a single paragraph, as the DAAW format requires. -->
Claude Code. Assistance given to the author, AI.
I used the following prompt in Claude Code, Anthropic's AI coding assistant, run inside VS Code: "Based on the kaggle_prompt and the README, help me structure this folder."
The prompt returned an inspection of my project folder and the competition data.
It found that the 16,384 feature columns are a 64x64 spectrogram stored as identical RGB channels plus a constant alpha channel, so only 4,096 grayscale values carry information.
It also identified setup errors in my repository: my .gitignore had been created as a folder instead of a file, my requirements.txt contained description text instead of package names, and my notebook files were empty.
The AI corrected these files.
It wrote starter Python modules for data loading, feature scaling and PCA, model pipelines (LDA, Logistic Regression, KNN, Decision Tree, and linear and RBF SVMs), and cross-validated ROC AUC evaluation.
It also wrote four starter Jupyter notebooks (EDA, baseline comparison, SVM tuning, and final submission) and an updated README with a first 5-fold cross-validation baseline comparison.
In follow-up prompts I asked the AI to "commit this to the github" and "just merge into master and push it for me," and it ran those git commands.
I also asked it to "explain how gitignore and gitkeep works and why you use it," and it explained how those files keep raw data and credentials out of the repository while preserving the folder structure.
I then asked it to write this DAAW citation and to export a transcript of the conversation.
The complete conversation, including every prompt I gave and every response the AI returned, is recorded in the accompanying transcript ([Transcript.md](Transcript.md), in this folder).
The AI-generated code was used as the starting framework for the project's data processing, model comparison, and submission pipeline.
I ran the notebooks myself, which generated the class-mean spectrogram and ROC comparison figures and my submission file of predicted probabilities for the 200 test recordings.
The project structure, starter code, and git setup were produced with the AI's assistance as described above, and I used that output as a foundation for running, evaluating, and submitting my models.
Anthropic, (https://claude.ai). West Point, NY, 24OCT2026.
