package org.example;

public class Metric {
    private double inputTasks = 0; // число заявок, поступивших в систему
    private double processedTasks = 0; // число заявок, обслуженных системой
    private double missedTasks = 0; // число потерянных заявок.
    private double downtime = 0; // время простоя вычислительной системы
    private double totalTime = 0;
    private double probabilityOfProcessing = 0; // вероятность обслуживания пакета
    private double probabilityOfFailure = 0; // вероятность отказа;

    public Metric() {
    }

    public Metric(double inputTasks, double processedTasks, double missedTasks, double downtime, double probabilityOfProcessing, double probabilityOfFailure) {
        this.inputTasks = inputTasks;
        this.processedTasks = processedTasks;
        this.missedTasks = missedTasks;
        this.downtime = downtime;
        this.probabilityOfProcessing = probabilityOfProcessing;
        this.probabilityOfFailure = probabilityOfFailure;
    }

    public double getInputTasks() {
        return inputTasks;
    }

    public void incInputTasks() {
        this.inputTasks++;
        calculateProbabilityOfProcessing();
        calculateProbabilityOfFailure();
    }

    public double getProcessedTasks() {
        return processedTasks;
    }

    public void incProcessedTasks() {
        this.processedTasks++;
        calculateProbabilityOfProcessing();
    }

    public double getMissedTasks() {
        return missedTasks;
    }

    public void incMissedTasks() {
        this.missedTasks++;
        calculateProbabilityOfFailure();
    }

    public double getDowntime() {
        return downtime;
    }

    public void incDowntime(double delta) {
        this.downtime += delta;
    }

    public double getProbabilityOfProcessing() {
        return probabilityOfProcessing;
    }

    public double getProbabilityOfFailure() {
        return probabilityOfFailure;
    }

    private void calculateProbabilityOfProcessing() {
        this.probabilityOfProcessing = this.processedTasks / this.inputTasks;
    }

    private void calculateProbabilityOfFailure() {
        this.probabilityOfFailure = this.missedTasks / this.inputTasks;
    }

    @Override
    public String toString() {
        return "Metrics{" +
                "\n\t inputTasks:\t\t" + inputTasks +
                ",\n\t processedTasks:\t" + processedTasks +
                ",\n\t missedTasks: \t\t" + missedTasks +
                ",\n\t downtime: \t\t\t" + downtime +
                ",\n\t Probability of processing: \t" + probabilityOfProcessing +
                ",\n\t Probability of failure: \t\t" + probabilityOfFailure +
                "\n}\n";
    }
}
