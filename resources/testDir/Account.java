class Account
{
	private String name;
	private int accNumber;
	private double balance;


	public Account(int newAccNumber, String newName, double startBal)
	{
		accNumber= newAccNumber;
		name = newName;
		balance= startBal;
	}

	public double getBalance()
	{
		return balance;
	}

	public int getAccNumber()
	{
		return accNumber;
	}


	public void setBalance(double newBal)
	{
		balance=newBal;
	}

	public void setName(String newName)
	{
		name=newName;
	}
}

