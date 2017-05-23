import java.util.Scanner;
class Assignment3
{
	public static void main(String args[])
	{
		Scanner kbd= new Scanner(System.in);
		
		String restaurantName;
		double foodBill, barBill, tip, barTax, foodTax, grandTotal, amountPerPerson;
		int numOfPeople;
		
		final double TAXES=0.14;
		final double FOODTIP= 0.20;
		final double BARTIP= 0.10;
		
		
		
		
		/*
		final means its a CONSTANT variables which means you CANNOT change the value inside it
		so if you did something like this
		TAXES=3; 
		you will not be able to compile it
		capitilizing taxes DOESN'T affect your code 
		it is just there to let whoever reads it know that it is a constant variable
		it's just a notation
		writing
		final taxes= 0.14 
		is similar to 
		final TAXES=0.14
		*/
		
		
		//Here is where we get the user input
		System.out.println("Enter restaurant name");
		restaurantName=kbd.next();
		
		System.out.println("Enter food bill");
		foodBill=kbd.nextDouble();
		
		System.out.println("Enter bar bill");
		barBill=kbd.nextDouble();
		
		System.out.println("Enter number of people");
		numOfPeople=kbd.nextInt();
		
		
		//Now we do the calculations
		foodTax= foodBill * TAXES;
		barTax= barBill * TAXES;
		tip =  (barBill*BARTIP) + (foodBill*FOODTIP);// total of 10% of the bar bill and 20% of the food bill, not including any taxes
		grandTotal= foodBill+ foodTax + barBill + barTax + tip;
		
		amountPerPerson=grandTotal/numOfPeople;
		
		//Here is the output
		System.out.println("Restaurant name " + restaurantName);
		System.out.println("The tax rate is $ " + TAXES);
		System.out.println("The tax for food bill is $ " + foodTax);
		System.out.println("The tax for bar bill is $ " + barTax);
		System.out.println("The tip is $ " + tip);
		System.out.println("The grand total is $ " + grandTotal);
		System.out.println("The amount for each person is $ " + amountPerPerson);
		
		
		
		
		
		
	}

}