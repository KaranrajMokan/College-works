package com.spm.cbe;

import java.util.ArrayList;

public class ProjectCosts {
    public ArrayList<ArrayList<Integer>> costOfProjectsPerYear;
    public ArrayList<Integer> netProfitForProjects;

    public ProjectCosts(){
        costOfProjectsPerYear = new ArrayList<>();
        netProfitForProjects = new ArrayList<>();
    }

    public void addCostPerYear(ArrayList<Integer> costPerYear){
        costOfProjectsPerYear.add(new ArrayList<>(costPerYear));
    }

    public void addNetProfit(ArrayList<Integer> netProfits){
        netProfitForProjects.addAll(netProfits);
    }

    public void printCosts(){
        int count=0;
        StringBuilder printString = new StringBuilder("Year\t");
        for(int i=1;i<=costOfProjectsPerYear.get(0).size();i++){
            String temp="Project"+i+"\t\t";
            printString.append(temp);
        }
        System.out.println(printString);
        for (ArrayList<Integer> integers : costOfProjectsPerYear) {
            System.out.print(count);
            for (Integer integer : integers) {
                System.out.print(String.format("%" + 15 + "s",integer));
            }
            System.out.println();
            count++;
        }
        System.out.print("NP");
        int initialCount=0;
        for(Integer integers: netProfitForProjects) {
            if (initialCount == 0) {
                System.out.print(String.format("%" + 14 + "s", integers));
                initialCount++;
            }
            else
                System.out.print(String.format("%" + 15 + "s", integers));
        }
        System.out.println();
    }
}
