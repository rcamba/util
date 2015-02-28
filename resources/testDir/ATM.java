import java.util.Scanner;
class ATM
{
	
	final int BALANCE=1;
	final int DEPOSIT=2;
	final int WITHDRAW=3;
	boolean accountValid(int accountNum, int pinNumber)
	{
		boolean result;

		if( acc.getAccNumber()==accountNum && card.getPin()==pinNumber)
			result=true;
		else
			result=false;
		return result;		
	}

	double balance(int accountNumber, int pinNumber)
	{
		double resultValue;
		if( accountValid(accountNumber, pinNumber)==false)
			resultValue=Double.NaN;
		else
		{
			resultValue =  acc.getBalance();
		}

		return resultValue;
	}

	boolean deposit(int accountNumber, int pinNumber, double amount)
	{
		boolean result=true;
		
		if( accountValid(accountNumber, pinNumber)==false)
			result=false;

		else if(amount<0)
			result=false;

		else
		{

			acc.setBalance( acc.getBalance() + amount);
		}	
			

		return result;
	}

	boolean withdraw (int accNumber, int pinNumber, double amount)
	{
		boolean result=true;
		
		if ( accountValid(accNumber,pinNumber)==false)
			result=false;
		else if(amount < 0)
			result=false;
		else if (amount > acc.getBalance())
			result=false;
		else
			acc.setBalance( acc.getBalance() - amount);
			

		return result;
	}


	
	public void run()
	{
		int userAccNum, userPinNum, transacChoice, amount;
		boolean keepGoing=true;
		String continueTransac="";
		Scanner kbd= new Scanner(System.in);
		
		

		do
		{
			System.out.println("Enter account number");
			userAccNum=Integer.parseInt(kbd.nextLine());
			System.out.println("Enter pin number");
			userPinNum=Integer.parseInt(kbd.nextLine());

			if(accountValid(userAccNum, userPinNum)==false)
			{
				System.out.println("Invalid account information: " + userAccNum +" " +userPinNum );

			}

			else
			{
				System.out.println("Enter type of transaction: \n");
				System.out.println("[1]Balance");
				System.out.println("[2]Deposit");
				System.out.println("[3]Withdrawal");
				transacChoice=Integer.parseInt(kbd.nextLine());

				if(transacChoice==1)
				{
					System.out.println("Your current balance is: " + balance(userAccNum, userPinNum));

				}

				else if(transacChoice==2)
				{
					System.out.println("Enter amount to deposit");
					amount=Integer.parseInt(kbd.nextLine());
					deposit(userAccNum, userPinNum,amount);					
				}

				else if(transacChoice==3)
				{
					System.out.println("Enter amount to withdraw");
					amount=Integer.parseInt(kbd.nextLine());
					withdraw(userAccNum, userPinNum,amount);					
				}

				else
				{
					System.out.println("Invalid choice");
				}

				System.out.println("Press 'y' to continue or 'n' to stop");
				continueTransac=kbd.nextLine();
				if (continueTransac.equals("y"))
				{
					keepGoing=true;
				}

				else
					keepGoing=false;
			}
			
		} while(keepGoing==true);
	}

	private Account acc;
	private ATM_Card card;
	public ATM()
	{
		acc= new Account(654789,"Bob", 101.99);
		card= new ATM_Card(acc.getAccNumber(), 2222);		
	}

}