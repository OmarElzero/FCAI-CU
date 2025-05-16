using System.Data;
using System.Data.SqlClient;

namespace ERDApp
{
    public class Database
    {
        private string connectionString = "Server=YOUR_SERVER;Database=YOUR_DATABASE;Trusted_Connection=True;";

        public DataTable GetClients()
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                SqlDataAdapter da = new SqlDataAdapter("SELECT * FROM Client", conn);
                DataTable dt = new DataTable();
                da.Fill(dt);
                return dt;
            }
        }

        public void AddClient(string name, string phone, string address, string paymentInfo)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                SqlCommand cmd = new SqlCommand("INSERT INTO Client (Name, Phone, Address, PaymentInfo) VALUES (@Name, @Phone, @Address, @PaymentInfo)", conn);
                cmd.Parameters.AddWithValue("@Name", name);
                cmd.Parameters.AddWithValue("@Phone", phone);
                cmd.Parameters.AddWithValue("@Address", address);
                cmd.Parameters.AddWithValue("@PaymentInfo", paymentInfo);
                cmd.ExecuteNonQuery();
            }
        }

        public void UpdateClient(int clientId, string name, string phone, string address, string paymentInfo)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                SqlCommand cmd = new SqlCommand("UPDATE Client SET Name=@Name, Phone=@Phone, Address=@Address, PaymentInfo=@PaymentInfo WHERE ClientID=@ClientID", conn);
                cmd.Parameters.AddWithValue("@Name", name);
                cmd.Parameters.AddWithValue("@Phone", phone);
                cmd.Parameters.AddWithValue("@Address", address);
                cmd.Parameters.AddWithValue("@PaymentInfo", paymentInfo);
                cmd.Parameters.AddWithValue("@ClientID", clientId);
                cmd.ExecuteNonQuery();
            }
        }

        public void DeleteClient(int clientId)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();
                SqlCommand cmd = new SqlCommand("DELETE FROM Client WHERE ClientID=@ClientID", conn);
                cmd.Parameters.AddWithValue("@ClientID", clientId);
                cmd.ExecuteNonQuery();
            }
        }
    }
}
