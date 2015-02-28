import java.io.*;
import java.util.*;
import java.text.*;
class A2Q2
{
	public static void main(String [] args)
	{
		Scanner kbd= new Scanner(System.in);
		String input, tempStr, temp;
		String [] tempArray, sortedArray;;
		int i=0, j=0;		
				
			
		//testSA();
		//testBA();
		//testMultiDimArray();
		testNull();
		/*
		System.out.println("Enter three words that are four letters long separated by spaces");
		
		input=kbd.nextLine();
		
		while (input.length()!=14 || input.charAt(4)!=' ' || input.charAt(9)!=' ')
		{
			System.out.println("Invalid input");
			System.out.println("Enter three words that are four letters long separated by spaces");
			input=kbd.nextLine();
		}
		*/
		
		
		//input="Orange Red Blue";
		/*
		input="Black,Fire,Cow";
		
		tempArray=input.split(",");
		
		
		for(int r=0; r<tempArray.length; r++)
			System.out.println(tempArray[r]);
			
		
		
		while (i<tempArray.length)
		{
			j=0;
			while(j<tempArray.length)
			{
				if (tempArray[i].compareTo(tempArray[j]) < 0 )
				{
					temp=tempArray[i];
					tempArray[i]=tempArray[j];
					tempArray[j]=temp;
					
				}
				
				j=j+1;
			}
			i=i+1;
		}
		*/
		
		/*
		if (tempArray[0].compareTo(tempArray[1])<0)
		{
			temp=tempArray[0];
			tempArray[0]=tempArray[1];
			tempArray[1]=temp;
		}
		
		if (tempArray[0].compareTo(tempArray[2])<0)
		{
			temp=tempArray[0];
			tempArray[0]=tempArray[2];
			tempArray[2]=temp;
		}
		
		//separator
		
		if (tempArray[1].compareTo(tempArray[2])<0)
		{
			temp=tempArray[1];
			tempArray[1]=tempArray[2];
			tempArray[2]=temp;
		}
		
		if (tempArray[1].compareTo(tempArray[0])<0)
		{
			
			tempArray[1]=tempArray[0];
			tempArray[0]=tempArray[1];
			
		}
		
		//separator
		
		if (tempArray[2].compareTo(tempArray[0])<0)
		{
			temp=tempArray[2];
			tempArray[2]=tempArray[0];
			tempArray[0]=temp;
		}
		
		if (tempArray[2].compareTo(tempArray[1])<0)
		{
			temp=tempArray[2];
			tempArray[2]=tempArray[1];
			tempArray[1]=temp;
		}
		
		
		for(int r=0; r<tempArray.length; r++)
			System.out.println(tempArray[r]);
		
		*/
		//greater = past the word in the dictionary
		//before the word in the dictionary
		//Dime, Blue, Keys
	}
	
	public static void testSA()
	{
		String s="1!2!3!4!5!6!7!8!9!", temp="";
		String [] strArray;
		int i=0, j=0;
		
		strArray=s.split("!");
		
		while (i<strArray.length)
		{
			j=0;
			while(j<strArray.length)
			{
				if ( Integer.parseInt(strArray[i]) > Integer.parseInt(strArray[j]) )
				//if (strArray[i].compareTo(strArray[j]) > 0)
				{
					temp=strArray[i];
					strArray[i]=strArray[j];
					strArray[j]=temp;
					
				}
				
				j=j+1;
			}
			i=i+1;
		}
		
		
		for(int k=0; k<strArray.length; k++)
			System.out.println(strArray[k]);
	}
	
	public static void testBA()
	{
		try {  
			String str_date="1965/03/04";
			DateFormat formatter ; 
			Date date , date2; 
			formatter = new SimpleDateFormat("yyyy/MM/dd");
			date = (Date)formatter.parse(str_date);  
			
			str_date="2005/03/04";
			
			
			formatter = new SimpleDateFormat("yyyy/MM/dd");
			date2 = (Date)formatter.parse(str_date);  
			
			System.out.println(date.before(date2) );
			System.out.println(date2);
		} 
		catch (ParseException e)
		{
			System.out.println("Exception :"+e);  
		}
		
		
	}
	
	public static void testMultiDimArray()
	{
		int [][] multiArray=new int[3][3];
		
		for(int i=0;i<multiArray.length;i++)
			for(int j=0; j< multiArray[i].length; j++)
				if (j%2==0)
					multiArray[i][j]=1;
				else
					multiArray[i][j]=9;
				
				
		for(int i=0;i<multiArray.length;i++)
		{
			for(int j=0; j< multiArray[i].length; j++)
				System.out.print(multiArray[i][j]);
			System.out.println();
		}
	}
	
	public static void testNull()
	{
		LinkedList b=new LinkedList();
		
		testInsertInAnotherMethod(b);
		System.out.println(b);
	}
	
	public static void testInsertInAnotherMethod(LinkedList kj)
	{
		LinkedList r=new LinkedList();
		
		r.insert(888);
		r.insert(818);
		
		
		kj=r;
		System.out.println(kj);
		//kj.insert(2);
		//kj.insert(3);
	}
}