import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Swig's Sorting Algorithm")

        self.mode = tk.StringVar()
        self.num_elements = tk.IntVar(value=30)
        self.visualize = tk.BooleanVar(value=True)

        modes = ['Bubble Sort', 'Quick Sort', 'Merge Sort', 'Insertion Sort', 'Selection Sort', 'Heap Sort', 'Swigs Custom']
        mode_label = ttk.Label(root, text="Select Sorting Algorithm:")
        mode_label.grid(row=0, column=0, padx=5, pady=5)
        mode_combobox = ttk.Combobox(root, textvariable=self.mode, values=modes)
        mode_combobox.grid(row=0, column=1, padx=5, pady=5)

        num_label = ttk.Label(root, text="Number of Elements:")
        num_label.grid(row=1, column=0, padx=5, pady=5)
        num_entry = ttk.Entry(root, textvariable=self.num_elements)
        num_entry.grid(row=1, column=1, padx=5, pady=5)

        visualize_checkbox = ttk.Checkbutton(root, text="Visualize", variable=self.visualize)
        visualize_checkbox.grid(row=2, column=0, padx=5, pady=5)

        start_button = ttk.Button(root, text="Start", command=self.start_sorting)
        start_button.grid(row=2, column=1, padx=5, pady=5)

    def start_sorting(self):
        elements = [random.randint(1, 100) for _ in range(self.num_elements.get())]
        algorithm = self.mode.get()

        if algorithm == "Bubble Sort":
            self.run_sort(elements, self.bubble_sort, "Bubble Sort")
        elif algorithm == "Quick Sort":
            self.run_sort(elements, self.quick_sort, "Quick Sort")
        elif algorithm == "Merge Sort":
            self.run_sort(elements, self.merge_sort, "Merge Sort")
        elif algorithm == "Insertion Sort":
            self.run_sort(elements, self.insertion_sort, "Insertion Sort")
        elif algorithm == "Selection Sort":
            self.run_sort(elements, self.selection_sort, "Selection Sort")
        elif algorithm == "Heap Sort":
            self.run_sort(elements, self.heap_sort, "Heap Sort")
        elif algorithm == "Swigs Custom":
            self.run_sort(elements, self.custom_algorithm, "Swigs Custom")



    def run_sort(self, elements, sort_function, algorithm_name):
        if self.visualize.get():
            self.visualize_sort(elements, sort_function, algorithm_name)
        else:
            start_time = time.time()
            comparisons = {'count': 0}
            confirmed = [False] * len(elements)
            generator = sort_function(elements, comparisons, confirmed)
            for _ in generator:
                pass
            duration = time.time() - start_time
            self.show_summary(algorithm_name, len(elements), comparisons['count'], duration)

    def visualize_sort(self, elements, sort_function, algorithm_name):
        fig, ax = plt.subplots()
        bars = ax.bar(range(len(elements)), elements)
        comparisons = {'count': 0}
        confirmed = [False] * len(elements)
        start_time = time.time()
    
        def update(elements):
            try:
                next_state = next(generator)
                for index, (bar, height) in enumerate(zip(bars, next_state)):
                    bar.set_height(height)
                    if index < len(confirmed):
                        bar.set_color('green' if confirmed[index] else 'blue')
            except StopIteration:
                end_time = time.time()
                duration = end_time - start_time
                self.show_summary(algorithm_name, len(elements), comparisons['count'], duration)
                ani.event_source.stop()
    
        generator = sort_function(elements, comparisons, confirmed)
        ani = animation.FuncAnimation(fig, func=lambda _: update(elements), frames=len(elements) ** 2, interval=20, repeat=False)
        plt.show()


    def show_summary(self, algorithm_name, total_elements, total_comparisons, duration):
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Sorting Summary")

        summary_label = ttk.Label(summary_window, text=f"Algorithm: {algorithm_name}")
        summary_label.grid(row=0, column=0, padx=10, pady=5)
        
        elements_label = ttk.Label(summary_window, text=f"Total Elements: {total_elements}")
        elements_label.grid(row=1, column=0, padx=10, pady=5)
        
        comparisons_label = ttk.Label(summary_window, text=f"Total Comparisons: {total_comparisons}")
        comparisons_label.grid(row=2, column=0, padx=10, pady=5)
        
        duration_label = ttk.Label(summary_window, text=f"Time Taken: {duration:.4f} seconds")
        duration_label.grid(row=3, column=0, padx=10, pady=5)

    def custom_algorithm(self, elements, comparisons, confirmed):
        n = len(elements)
        group_size = 10

        def is_sorted(lst):
            for i in range(len(lst) - 1):
                if lst[i] > lst[i + 1]:
                    return False
            return True

        while not is_sorted(elements):
            for i in range(0, n, group_size):
                group = elements[i:i + group_size]
                group.sort()
                elements[i:i + group_size] = group
                for j in range(i, min(i + group_size, n)):
                    confirmed[j] = False

                for j in range(i, min(i + group_size, n)):
                    confirmed[j] = True
                comparisons['count'] += len(group) * (len(group) - 1) // 2
                yield elements
            if is_sorted(elements):
                break
            group_size = min(n, group_size + (n // 10))

    def bubble_sort(self, elements, comparisons, confirmed):
        n = len(elements)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                comparisons['count'] += 1
                if elements[j] > elements[j + 1]:
                    elements[j], elements[j + 1] = elements[j + 1], elements[j]
                    swapped = True
                    yield elements
            confirmed[n - i - 1] = True
            if not swapped:
                for k in range(n - i - 1):
                    confirmed[k] = True
                yield elements
                break

    def quick_sort(self, elements, comparisons, confirmed, low=0, high=None):
        if high is None:
            high = len(elements) - 1

        def partition(low, high):
            pivot = elements[high]
            i = low - 1
            for j in range(low, high):
                comparisons['count'] += 1
                if elements[j] < pivot:
                    i += 1
                    elements[i], elements[j] = elements[j], elements[i]
                    yield elements
            elements[i + 1], elements[high] = elements[high], elements[i + 1]
            yield elements
            return i + 1

        def quicksort_recursive(low, high):
            if low < high:
                pivot_index = yield from partition(low, high)
                confirmed[pivot_index] = True
                yield from quicksort_recursive(low, pivot_index - 1)
                yield from quicksort_recursive(pivot_index + 1, high)
            else:
                if low == high:
                    confirmed[low] = True

        return quicksort_recursive(low, high)

    def merge_sort(self, elements, comparisons, confirmed):
        if len(elements) > 1:
            mid = len(elements) // 2
            left_half = elements[:mid]
            right_half = elements[mid:]

            yield from self.merge_sort(left_half, comparisons, confirmed)
            yield from self.merge_sort(right_half, comparisons, confirmed)

            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                comparisons['count'] += 1
                if left_half[i] < right_half[j]:
                    elements[k] = left_half[i]
                    i += 1
                else:
                    elements[k] = right_half[j]
                    j += 1
                k += 1
                yield elements

            while i < len(left_half):
                elements[k] = left_half[i]
                i += 1
                k += 1
                yield elements

            while j < len(right_half):
                elements[k] = right_half[j]
                j += 1
                k += 1
                yield elements

            confirmed[:] = [True] * len(elements)

    def insertion_sort(self, elements, comparisons, confirmed):
        for i in range(1, len(elements)):
            key = elements[i]
            j = i - 1
            while j >= 0 and key < elements[j]:
                comparisons['count'] += 1
                elements[j + 1] = elements[j]
                j -= 1
                yield elements
            elements[j + 1] = key
            confirmed[i] = True
            yield elements

    def selection_sort(self, elements, comparisons, confirmed):
        for i in range(len(elements)):
            min_idx = i
            for j in range(i + 1, len(elements)):
                comparisons['count'] += 1
                if elements[j] < elements[min_idx]:
                    min_idx = j
            elements[i], elements[min_idx] = elements[min_idx], elements[i]
            confirmed[i] = True
            yield elements

    def heap_sort(self, elements, comparisons, confirmed):
        def heapify(n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and elements[left] > elements[largest]:
                largest = left
            if right < n and elements[right] > elements[largest]:
                largest = right
            if largest != i:
                elements[i], elements[largest] = elements[largest], elements[i]
                yield elements
                yield from heapify(n, largest)

        n = len(elements)
        for i in range(n // 2 - 1, -1, -1):
            yield from heapify(n, i)

        for i in range(n - 1, 0, -1):
            elements[i], elements[0] = elements[0], elements[i]
            confirmed[i] = True
            yield elements
            yield from heapify(i, 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
