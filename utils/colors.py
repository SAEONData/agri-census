from utils.database import get_distinct_indicators
import random

def assign_colors(categories):
    """Assigns a consistent color to each item in a list."""
    base_colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b",
        "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ]
    color_map = {}
    for i, item in enumerate(sorted(categories)):
        color_map[item] = base_colors[i % len(base_colors)]
    return color_map

def get_indicator_colors():
    indicators = get_distinct_indicators("indicator")
    return assign_colors(indicators)

def get_sub_indicator_colors():
    sub_indicators = get_distinct_indicators("sub_indicator")
    return assign_colors(sub_indicators)

def get_sub_sub_indicator_colors():
    sub_sub_indicators = get_distinct_indicators("sub_sub_indicator")
    return assign_colors(sub_sub_indicators)
