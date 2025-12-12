using System;
using System.Data;
using System.Data.SqlClient;
using System.Windows.Forms;

namespace ERDApp
{
    public partial class MainForm : Form
    {
        private Database db;
        public MainForm()
        {
            InitializeComponent();
            db = new Database();
            LoadClients();
        }

        private void LoadClients()
        {
            var dt = db.GetClients();
            dataGridViewClients.DataSource = dt;
        }

        private void buttonAdd_Click(object sender, EventArgs e)
        {
            db.AddClient(textBoxName.Text, textBoxPhone.Text, textBoxAddress.Text, textBoxPayment.Text);
            LoadClients();
        }

        private void buttonUpdate_Click(object sender, EventArgs e)
        {
            if (dataGridViewClients.SelectedRows.Count > 0)
            {
                int id = Convert.ToInt32(dataGridViewClients.SelectedRows[0].Cells["ClientID"].Value);
                db.UpdateClient(id, textBoxName.Text, textBoxPhone.Text, textBoxAddress.Text, textBoxPayment.Text);
                LoadClients();
            }
        }

        private void buttonDelete_Click(object sender, EventArgs e)
        {
            if (dataGridViewClients.SelectedRows.Count > 0)
            {
                int id = Convert.ToInt32(dataGridViewClients.SelectedRows[0].Cells["ClientID"].Value);
                db.DeleteClient(id);
                LoadClients();
            }
        }
    }
}
