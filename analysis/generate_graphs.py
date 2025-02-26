import matplotlib.pyplot as plt

def plot_bar_chart(subjects, scores):
    plt.figure(figsize=(8, 5))
    plt.bar(subjects, scores, color='skyblue')
    plt.xlabel('Subjects')
    plt.ylabel('Scores')
    plt.title('Subject-wise Scores')
    plt.show()
