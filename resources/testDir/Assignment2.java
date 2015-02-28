import java.util.Scanner;
class Assignment2
{
	public static void main(String args[])
	{
		String initTime, finalTime, temp;
		int initHour, initMinute, finHour, finMinute, diffHour, diffMinute;
		
		Scanner kbd= new Scanner(System.in);
		
		System.out.println("Enter the initial time");
		initTime=kbd.nextLine();
		
		System.out.println("Enter the final time");
		finalTime=kbd.nextLine();
		
		initHour= Integer.parseInt ( Character.toString( initTime.charAt(0) ) + Character.toString( initTime.charAt(1)) );
		initMinute= Integer.parseInt ( Character.toString( initTime.charAt(2) ) + Character.toString( initTime.charAt(3)) );
		
		finHour= Integer.parseInt ( Character.toString( finalTime.charAt(0) ) + Character.toString( finalTime.charAt(1)) );
		finMinute= Integer.parseInt ( Character.toString( finalTime.charAt(2) ) + Character.toString( finalTime.charAt(3)) );
		
		//calculating the difference
		diffHour=finHour-initHour;
		diffMinute=finMinute-initMinute;
		
		System.out.println("The difference in hours is: " +diffHour);
		System.out.println("The difference in minutes is: " +diffMinute);
	}

}