package org.example;

import java.util.ArrayList;
import java.util.List;
import java.util.function.ToDoubleFunction;

public class Main {
    private static final int numberOfSimulations = 85;

    private static double getAvg(List<Metric> metrics, ToDoubleFunction<Metric> mapper) {
        return metrics.stream()
                .mapToDouble(mapper)
                .average()
                .orElse(0);
    }

    private static double getDispercionaAvg(List<Metric> metrics, int numberOfSimulations, double avg, ToDoubleFunction<Metric> mapper) {
        return metrics.stream()
                .mapToDouble(m -> Math.pow(avg - mapper.applyAsDouble(m), 2))
                .sum() / (numberOfSimulations - 1);
    }

    private static Metric getSampleAvgMetric(List<Metric> metrics) {
        return new Metric(
                getAvg(metrics, Metric::getInputTasks),
                getAvg(metrics, Metric::getProcessedTasks),
                getAvg(metrics, Metric::getMissedTasks),
                getAvg(metrics, Metric::getDowntime),
                getAvg(metrics, Metric::getProbabilityOfProcessing),
                getAvg(metrics, Metric::getProbabilityOfFailure)
        );
    }

    private static Metric getDisperionAvgMetric(List<Metric> metrics) {
        var sampleAvgMetric = getSampleAvgMetric(metrics);

        return new Metric(
                getDispercionaAvg(metrics, numberOfSimulations, sampleAvgMetric.getInputTasks(), Metric::getInputTasks),
                getDispercionaAvg(metrics, numberOfSimulations, sampleAvgMetric.getProcessedTasks(), Metric::getProcessedTasks),
                getDispercionaAvg(metrics, numberOfSimulations, sampleAvgMetric.getMissedTasks(), Metric::getMissedTasks),
                getDispercionaAvg(metrics, numberOfSimulations, sampleAvgMetric.getDowntime(), Metric::getDowntime),
                getDispercionaAvg(metrics, numberOfSimulations, sampleAvgMetric.getProbabilityOfProcessing(), Metric::getProbabilityOfProcessing),
                getDispercionaAvg(metrics, numberOfSimulations, sampleAvgMetric.getProbabilityOfFailure(), Metric::getProbabilityOfFailure)
        );
    }

    public static void main(String[] args) {
        var model = new ModelSimulation();
        var metrics = new ArrayList<Metric>(numberOfSimulations);

        for (int i = 0; i < numberOfSimulations; i++) {
            model.runSimulation();
            metrics.add(model.getMetrics());
        }

        System.out.println("Sample Avg metrics: \n" + getSampleAvgMetric(metrics));
        System.out.println("Dispersion Avg metrics: \n" + getDisperionAvgMetric(metrics));
    }
}