package com.spm.cbe;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Dictionary;
import java.util.Enumeration;

public class CostBenefitEvaluation {
    ProjectCosts projectCosts;

    public CostBenefitEvaluation(ProjectCosts projectCosts) {
        this.projectCosts = projectCosts;
    }

    public int calculateNetProfit() {
        ArrayList<Integer> netProfits = projectCosts.netProfitForProjects;
        int maximumNetProfit = Collections.max(netProfits);
        return netProfits.indexOf(maximumNetProfit) + 1;
    }

    public int[] calculatePaybackPeriod() {
        ArrayList<Integer> initialInvestment = projectCosts.costOfProjectsPerYear.get(0);
        int[] result = new int[2];
        for (int i = 1; i < projectCosts.costOfProjectsPerYear.size(); i++) {
            ArrayList<Integer> costForYears = projectCosts.costOfProjectsPerYear.get(i);
            for (int j = 0; j < costForYears.size(); j++) {
                System.out.print(initialInvestment.get(j));
                System.out.print(" + " + costForYears.get(j));
                initialInvestment.set(j, initialInvestment.get(j) + costForYears.get(j));
                System.out.println(" = " + initialInvestment.get(j));
                if (initialInvestment.get(j) >= 0) {
                    result[0] = j + 1;
                    result[1] = i;
                    return result;
                }
            }
        }
        return result;
    }

    public double[] calculateReturnOnInvestment() {
        double numberOfYears = projectCosts.costOfProjectsPerYear.size() - 1;
        ArrayList<Integer> initialInvestment = projectCosts.costOfProjectsPerYear.get(0);
        ArrayList<Integer> netProfit = projectCosts.netProfitForProjects;
        double highestROI = 0;
        double highestProject = 0;
        for (int i = 0; i < netProfit.size(); i++) {
            double averageAnnualProfit = netProfit.get(i) / numberOfYears;
            double currentROI = (averageAnnualProfit / Math.abs(initialInvestment.get(i))) * 100;
            if (currentROI > highestROI) {
                highestROI = currentROI;
                highestProject = i + 1;
            }
        }
        return new double[]{highestProject, highestROI};
    }

    public int[] calculateNetPresentValue(int discountPercent, Dictionary<Integer, ArrayList<Double>> discountRates) {
        ArrayList<Double> discounts = discountRates.get(discountPercent);
        ArrayList<Double> resultingNPV = new ArrayList<>();
        double sum;
        for (int i = 0; i < projectCosts.costOfProjectsPerYear.get(0).size(); i++) {
            sum = 0;
            for (int j = 0; j < projectCosts.costOfProjectsPerYear.size(); j++) {
                sum += projectCosts.costOfProjectsPerYear.get(j).get(i) * discounts.get(j);
            }
            resultingNPV.add((double) Math.round(sum));
        }
        double maximumNPV = Collections.max(resultingNPV);
        return new int[]{resultingNPV.indexOf(maximumNPV) + 1, (int) maximumNPV};
    }

    public void calculateInternalRateOfReturn(Dictionary<Integer, ArrayList<Double>> discountRates) {
        Enumeration<Integer> rates = discountRates.keys();
        ArrayList<ArrayList<Double>> discountValues = new ArrayList<>();
        ArrayList<Integer> discountKeys = new ArrayList<>();
        while(rates.hasMoreElements()){
            discountKeys.add(rates.nextElement());
        }
        Collections.sort(discountKeys);
        for (Integer discountKey : discountKeys) {
            discountValues.add(discountRates.get(discountKey));
        }
        ArrayList<ArrayList<Double>> totalNPV = new ArrayList<>();
        double sum;
        for (int i = 0; i < projectCosts.costOfProjectsPerYear.get(0).size(); i++) {
            ArrayList<Double> resultingNPV = new ArrayList<>();
            for (ArrayList<Double> discountValue : discountValues) {
                sum = 0;
                for (int j = 0; j < projectCosts.costOfProjectsPerYear.size(); j++) {
                    sum += projectCosts.costOfProjectsPerYear.get(j).get(i) * discountValue.get(j);
                }
                resultingNPV.add((double) Math.round(sum));
            }
            totalNPV.add(resultingNPV);
        }
        System.out.println("\nDiscount rates = " + discountKeys);
        for(ArrayList<Double> npv: totalNPV){
            System.out.println(npv);
        }
    }

}
