package com.spm.cbe;
import java.util.*;
import java.io.*;
import java.util.stream.Collectors;

public class Main {

    public static void scanner(ProjectCosts projectCosts){
        int numberOfYears, numberOfProjects;
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter the number of years");
        numberOfYears = scanner.nextInt();
        System.out.println("Enter the number of projects");
        numberOfProjects = scanner.nextInt();

        for (int i=0;i<=numberOfYears;i++){
            ArrayList<Integer> costPerYear = new ArrayList<>();
            System.out.println("Enter the cost for project for Year " + i);
            for (int j=0;j<numberOfProjects;j++){
                System.out.println("Project-"+(j+1)+":");
                costPerYear.add(scanner.nextInt());
            }
            projectCosts.addCostPerYear(costPerYear);
        }

        ArrayList<Integer> netProfit = new ArrayList<>();
        System.out.println("Enter the Net Profits for the projects");
        for (int j=0;j<numberOfProjects;j++){
            System.out.println("Project-"+(j+1)+":");
            netProfit.add(scanner.nextInt());
        }
        projectCosts.addNetProfit(netProfit);
        projectCosts.printCosts();
    }

    public static void file(ProjectCosts projectCosts) throws IOException {
        File file = new File("cost_sheet.txt");
        BufferedReader br = new BufferedReader(new FileReader(file));
        String string;
        while ((string = br.readLine()) != null) {
            String[] arrOfString = string.split(",");
            if (!arrOfString[0].equals("NP")) {
                ArrayList<Integer> arrOfInteger = Arrays.stream(arrOfString).map(Integer::valueOf).collect(Collectors.toCollection(ArrayList::new));
                arrOfInteger.remove(0);
                projectCosts.addCostPerYear(arrOfInteger);
            }
            else {
                String[] modifiedStringArray = Arrays.copyOfRange(arrOfString, 1, arrOfString.length);
                ArrayList<Integer> arrOfInteger = Arrays.stream(modifiedStringArray).map(Integer::valueOf).collect(Collectors.toCollection(ArrayList::new));
                projectCosts.addNetProfit(arrOfInteger);
            }
        }
    }

    public static void setDiscountRates(Dictionary<Integer,ArrayList<Double>> discountRates) throws IOException {
        File file = new File("discount_rates.txt");
        BufferedReader br = new BufferedReader(new FileReader(file));
        String string;
        ArrayList<String[]> readStringList = new ArrayList<>();
        while ((string = br.readLine()) != null) {
            readStringList.add(string.split(","));
        }
        for(int i=0;i<readStringList.get(0).length;i++) {
            ArrayList<Double> doubleList = new ArrayList<>();
            for (int j=1; j<readStringList.size(); j++) {
                doubleList.add(Double.valueOf(readStringList.get(j)[i]));
            }
            discountRates.put(Integer.valueOf(readStringList.get(0)[i]),doubleList);
        }
    }

    public static int netPresentValueHelper(Dictionary<Integer, ArrayList<Double>> discountRates){
        Scanner scanner = new Scanner(System.in);
        Enumeration<Integer> availableDiscounts = discountRates.keys();
        ArrayList<Integer> discountList = new ArrayList<>();
        System.out.println("\nEnter the discount rate for net present value method(Default is 10)");
        System.out.print("The available discount rates are ");
        while (availableDiscounts.hasMoreElements()) {
            discountList.add(availableDiscounts.nextElement());
        }
        Collections.sort(discountList);
        for(int i=0;i<discountList.size();i++){
            if(i!=discountList.size()-1)
                System.out.print(discountList.get(i)+",");
            else
                System.out.println(discountList.get(i));
        }
        int discountPercent = scanner.nextInt();
        if(!(discountList.contains(discountPercent)))
            discountPercent=10;

        return discountPercent;
    }

    public static void main(String[] args) throws IOException {
        int response = 0;
        Scanner scanner = new Scanner(System.in);
        ProjectCosts projectCosts = new ProjectCosts();
        Dictionary<Integer,ArrayList<Double>> discountRates = new Hashtable<>();
        System.out.println("Do you want to use Scanner(1) or file(2) for input?");
        System.out.println("Manual input should be given for scanner whereas no input is needed for file");
        System.out.println("Type 1 for Scanner, 2 for File");
        while (response != 1 && response != 2) {
            response = scanner.nextInt();
            switch (response) {
                case 1:
                    scanner(projectCosts);
                    break;
                case 2:
                    file(projectCosts);
                    break;
                default:
                    System.out.println("You did not choose a valid option. Please choose either Scanner(1) or File(2)");
                    break;
            }
        }
        setDiscountRates(discountRates);
        projectCosts.printCosts();
        CostBenefitEvaluation costBenefitEvaluation = new CostBenefitEvaluation(projectCosts);
        response=-1;
        int resultingProject;
        int[] resultingProjectAndDuration, resultingProjectAndNPV;
        double[] resultingProjectAndROI;
        while(response != 0){
            System.out.println("\nChoose one of the Cost Benefit Analysis methods.");
            System.out.println("1)Net Profit method\n2)Payback period\n3)Return on investment" +
                    "\n4)Net present value\n5)Internal rate of return\nType 0 to quit");
            response = scanner.nextInt();
            switch(response){
                case 0:
                    System.out.println("Thank you for using this application. The system shall exit now.");
                    break;
                case 1:
                    resultingProject = costBenefitEvaluation.calculateNetProfit();
                    System.out.println("\nAccording to the Net Profit method, PROJECT " + resultingProject
                            + " is chosen as it has the highest net profit value of " +
                            projectCosts.netProfitForProjects.get(resultingProject));
                    break;
                case 2:
                    resultingProjectAndDuration = costBenefitEvaluation.calculatePaybackPeriod();
                    System.out.println("\nAccording to the PayBack Period method, PROJECT " + resultingProjectAndDuration[0]
                            + " is chosen as it provides better payback period of " +
                            resultingProjectAndDuration[1]);
                    break;
                case 3:
                    resultingProjectAndROI = costBenefitEvaluation.calculateReturnOnInvestment();
                    System.out.println("\nAccording to the Return On Investment method, PROJECT "
                            + String.valueOf(resultingProjectAndROI[0]).replaceAll("0*$", "")
                                    .replaceAll("\\.$", "")
                            + " is chosen as it provides return on investment of " +
                            resultingProjectAndROI[1] + "%");
                    break;
                case 4:
                    int discountPercent = netPresentValueHelper(discountRates);
                    resultingProjectAndNPV = costBenefitEvaluation.calculateNetPresentValue(discountPercent,discountRates);
                    System.out.println("\nAccording to the Net Present Value method, PROJECT "
                            + resultingProjectAndNPV[0] + " is chosen as it has the highest net present value of " +
                            String.valueOf(resultingProjectAndNPV[1]).replaceAll("0*$", "")
                            .replaceAll("\\.$", ""));
                    break;
                case 5:
                    costBenefitEvaluation.calculateInternalRateOfReturn(discountRates);
                    break;
                default:
                    System.out.println("You did not choose the valid option");
                    break;
            }
        }
    }
}
