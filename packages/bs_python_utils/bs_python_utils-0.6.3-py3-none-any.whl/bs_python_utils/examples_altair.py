"""examples using my Altair functions"""

import numpy as np
from vega_datasets import data

from bs_python_utils.bs_altair import (
    alt_boxes,
    alt_density,
    alt_faceted_densities,
    alt_histogram_by,
    alt_histogram_continuous,
    alt_linked_scatterplots,
    alt_matrix_heatmap,
    alt_plot_fun,
    alt_scatterplot,
    alt_scatterplot_with_histo,
    alt_stacked_area,
    alt_stacked_area_facets,
    alt_superposed_faceted_densities,
    alt_superposed_faceted_lineplot,
    alt_superposed_lineplot,
    alt_tick_plots,
    plot_parameterized_estimates,
    plot_true_sim2_facets,
    plot_true_sim_facets,
)

cars = data.cars()

ch = alt_boxes(cars, "Horsepower", "Origin", "Year", save="../Graphs/cars_boxes")

ch = alt_superposed_lineplot(
    cars,
    "Horsepower",
    "Weight_in_lbs",
    "Origin",
    save="../Graphs/cars_superposed_lineplot",
)

ch = alt_superposed_faceted_lineplot(
    cars,
    "Horsepower",
    "Weight_in_lbs",
    "Origin",
    "Year",
    save="../Graphs/cars_superposed_faceted_lineplot",
)

ch = alt_superposed_faceted_densities(
    cars,
    "Horsepower",
    "Year",
    "Origin",
    save="../Graphs/cars_superposed_faceted_densities",
)


ch = alt_histogram_continuous(cars, "Horsepower", save="../Graphs/cars_histo_cont")

ch = alt_histogram_by(
    cars, "Origin", "Horsepower", str_agg="median", save="../Graphs/cars_histo_by"
)

elec = data.iowa_electricity()

ch = alt_stacked_area(
    elec,
    "year",
    "net_generation",
    "source",
    time_series=True,
    title="Generators",
    save="../Graphs/elec_stacked_areas",
)

ch = alt_stacked_area_facets(
    cars,
    "Year",
    "Displacement",
    "Name",
    "Origin",
    time_series=True,
    save="../Graphs/cars_stacked_areas_facets",
)

ch = alt_scatterplot(
    cars,
    "Year",
    "Displacement",
    time_series=True,
    title="Average car displacement",
    aggreg="average",
    save="../Graphs/cars_scatter",
)

ch = alt_scatterplot(
    cars,
    "Year",
    "Displacement",
    time_series=True,
    title="Average car displacement",
    aggreg="average",
    save="../Graphs/cars_scatter_labx",
    xlabel="Model year",
)

ch = alt_scatterplot(
    cars,
    "Horsepower",
    "Displacement",
    title="Car displacement",
    color="Origin",
    selection=True,
    save="../Graphs/cars_scatter_color",
    xlabel="Horsepower",
)

ch = alt_linked_scatterplots(
    cars,
    "Horsepower",
    "Displacement",
    "Miles_per_Gallon",
    "Origin",
    save="../Graphs/cars_linked_scatters",
)

ch = alt_scatterplot_with_histo(
    cars,
    "Horsepower",
    "Displacement",
    "Origin",
    save="../Graphs/cars_linked_scatter_histo",
)

ch = alt_density(cars, "Horsepower", save="../Graphs/horsepower_density")

ch = alt_faceted_densities(
    cars, "Horsepower", "Origin", save="../Graphs/horsepower_distribs"
)


def fnp(x):
    return x * x - 4.0


ch = alt_plot_fun(fnp, -2.0, 3.0, save="../Graphs/plot_function")

# test plot_parameterized_estimates
nvals = 50
vals_p = np.arange(nvals) / (nvals - 1.0)
true_vals = np.column_stack((vals_p, np.ones(nvals)))
estimates_a = np.random.normal(size=((nvals, 2)), scale=0.2) + vals_p.reshape((-1, 1))
estimates_b = np.random.normal(size=((nvals, 2)), scale=0.2) + np.ones((nvals, 2))
estimates = np.zeros((nvals, 2, 2))
estimates[..., 0] = estimates_a
estimates[..., 1] = estimates_b

ch = plot_parameterized_estimates(
    "Value of p",
    vals_p,
    ["a", "b"],
    true_vals,
    ["MLE", "MM"],
    estimates,
    colors=["black", "green", "blue"],
    save="../Graphs/ppe",
)

stats = np.reshape(estimates, (nvals, 4))
true_vals = stats + np.random.normal(loc=-0.1, scale=0.2, size=stats.shape)
ch = plot_true_sim_facets(
    "Value of p",
    vals_p,
    ["a", "b", "c", "d"],
    true_vals,
    stats,
    colors=["black", "red"],
    ncols=2,
    save="../Graphs/ptsf",
)

stats2 = stats + np.random.normal(loc=0.1, scale=0.2, size=stats.shape)
ch = plot_true_sim2_facets(
    "Value of p",
    vals_p,
    ["a", "b", "c", "d"],
    true_vals,
    stats,
    stats2,
    colors=["black", "red", "green"],
    ncols=2,
    save="../Graphs/pts2f",
)

ch = alt_tick_plots(cars, "Weight_in_lbs", save="../Graphs/weight_ticks")

ch = alt_tick_plots(
    cars, ["Horsepower", "Weight_in_lbs"], save="../Graphs/horse_weight_ticks"
)


mat = np.arange(24).reshape((4, 6))
ch = alt_matrix_heatmap(mat, "d", save="../Graphs/matrix_heatmap1")

ch = alt_matrix_heatmap(
    mat,
    ".2f",
    multiple=2.0,
    str_rows="X",
    str_cols="Y",
    title="XY float matrix",
    save="../Graphs/matrix_heatmap2",
)
