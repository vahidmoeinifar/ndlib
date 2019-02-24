from __future__ import absolute_import

import unittest
import past
import networkx as nx
import dynetx as dn

from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.mpl.PrevalenceComparison import DiffusionPrevalenceComparison
from ndlib.viz.mpl.TrendComparison import DiffusionTrendComparison
from ndlib.viz.mpl.PhasePlaneComparison import PhasePlaneComparison

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend

import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as epd
import ndlib.models.dynamic as dyn

from ndlib.viz.mpl.PhasePlane import PhasePlane
import os

__author__ = 'Giulio Rossetti'
__license__ = "BSD-2-Clause"
__email__ = "giulio.rossetti@gmail.com"


class MplVizTest(unittest.TestCase):

    def test_phaseplane(self):
        g = nx.barabasi_albert_graph(1000, 3)
        model = epd.SIRModel(g)
        config = mc.Configuration()
        config.add_model_parameter('beta', 0.05)
        config.add_model_parameter('gamma', 0.09)
        config.add_model_parameter("percentage_infected", 0.02)
        model.set_initial_status(config)
        iterations = model.iteration_bunch(1000)
        trends = model.build_trends(iterations)

        # Visualization
        viz = PhasePlane(model, trends, x="Susceptible", y="Infected")
        viz.plot("diffusion.pdf")
        os.remove("diffusion.pdf")

    def test_comp_phaseplane(self):
        g = nx.barabasi_albert_graph(1000, 3)

        model = epd.SIRModel(g)
        config = mc.Configuration()
        config.add_model_parameter('beta', 0.05)
        config.add_model_parameter('gamma', 0.09)
        config.add_model_parameter("percentage_infected", 0.02)
        model.set_initial_status(config)
        iterations = model.iteration_bunch(1000)
        trends = model.build_trends(iterations)

        model1 = epd.SIRModel(g)
        config = mc.Configuration()
        config.add_model_parameter('beta', 0.02)
        config.add_model_parameter('gamma', 0.01)
        config.add_model_parameter("percentage_infected", 0.06)
        model1.set_initial_status(config)
        iterations = model1.iteration_bunch(1000)
        trends1 = model.build_trends(iterations)

        # Visualization
        viz = PhasePlaneComparison([model, model1], [trends, trends1], x="Susceptible", y="Infected")
        viz.plot("diffusion.pdf")
        os.remove("diffusion.pdf")

    def test_visualize(self):
        g = nx.erdos_renyi_graph(1000, 0.1)
        model = epd.SIRModel(g)
        config = mc.Configuration()
        config.add_model_parameter('beta', 0.001)
        config.add_model_parameter('gamma', 0.01)
        config.add_model_parameter("percentage_infected", 0.05)
        model.set_initial_status(config)
        iterations = model.iteration_bunch(200)
        trends = model.build_trends(iterations)

        # Visualization
        viz = DiffusionTrend(model, trends)
        viz.plot("diffusion.pdf")
        os.remove("diffusion.pdf")

    def test_visualize_dynamic(self):
        dg = dn.DynGraph()

        for t in past.builtins.xrange(0, 4):
            g = nx.erdos_renyi_graph(200, 0.05)
            dg.add_interactions_from(g.edges(), t)

        model = dyn.DynSIModel(dg)
        config = mc.Configuration()
        config.add_model_parameter('beta', 0.1)
        config.add_model_parameter("percentage_infected", 0.1)
        model.set_initial_status(config)
        iterations = model.execute_snapshots()
        trends = model.build_trends(iterations)

        # Visualization
        viz = DiffusionPrevalence(model, trends)
        viz.plot("prevd.pdf")
        os.remove("prevd.pdf")

    def test_visualize_prevalence(self):
        g = nx.erdos_renyi_graph(1000, 0.1)
        model = epd.SIRModel(g)
        config = mc.Configuration()
        config.add_model_parameter('beta', 0.001)
        config.add_model_parameter('gamma', 0.01)
        config.add_model_parameter("percentage_infected", 0.05)
        model.set_initial_status(config)
        iterations = model.iteration_bunch(200)
        trends = model.build_trends(iterations)

        # Visualization
        viz = DiffusionPrevalence(model, trends)
        viz.plot("prev.pdf")
        os.remove("prev.pdf")

    def test_prevalence_comparison(self):

        # Network topology
        g = nx.erdos_renyi_graph(1000, 0.1)

        # Model selection
        model = epd.SIRModel(g)

        # Model Configuration
        cfg = mc.Configuration()
        cfg.add_model_parameter('beta', 0.001)
        cfg.add_model_parameter('gamma', 0.02)
        cfg.add_model_parameter("percentage_infected", 0.01)
        model.set_initial_status(cfg)

        iterations = model.iteration_bunch(200)
        trends = model.build_trends(iterations)

        model1 = epd.SIModel(g)
        cfg = mc.Configuration()
        cfg.add_model_parameter('beta', 0.001)
        cfg.add_model_parameter("percentage_infected", 0.01)
        model1.set_initial_status(cfg)

        iterations = model1.iteration_bunch(200)
        trends1 = model1.build_trends(iterations)

        viz = DiffusionPrevalenceComparison([model, model1], [trends, trends1])
        viz.plot("prev_comparison.pdf")
        os.remove("prev_comparison.pdf")

    def test_trend_comparison(self):

        # Network topology
        g = nx.erdos_renyi_graph(1000, 0.1)

        # Model selection
        model = epd.SIRModel(g)

        # Model Configuration
        cfg = mc.Configuration()
        cfg.add_model_parameter('beta', 0.001)
        cfg.add_model_parameter('gamma', 0.02)
        cfg.add_model_parameter("percentage_infected", 0.01)
        model.set_initial_status(cfg)

        iterations = model.iteration_bunch(200)
        trends = model.build_trends(iterations)

        model1 = epd.SIModel(g)
        cfg = mc.Configuration()
        cfg.add_model_parameter('beta', 0.001)
        cfg.add_model_parameter("percentage_infected", 0.01)
        model1.set_initial_status(cfg)

        iterations = model1.iteration_bunch(200)
        trends1 = model1.build_trends(iterations)

        viz = DiffusionTrendComparison([model, model1], [trends, trends1])

        viz.plot("trend_comparison.pdf")
        os.remove("trend_comparison.pdf")


if __name__ == '__main__':
    unittest.main()
