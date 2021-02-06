using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

using System.Windows.Threading;

namespace Flappy_Bird_Game
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        DispatcherTimer gameTimer = new DispatcherTimer();
        double score;
        int gravity = 8;
        bool gameOver;
        Rect flappyBirdHitBox;

        public MainWindow()
        {
            InitializeComponent();

            gameTimer.Tick += MainEventTimer;
            gameTimer.Interval = TimeSpan.FromMilliseconds(20);
            StartGame();
        }

        private void MainEventTimer(object sender, EventArgs e)
        {
            txtScore.Content = "Score: "+ score;

            flappyBirdHitBox = new Rect(Canvas.GetLeft(FlappyBird),Canvas.GetTop(FlappyBird), FlappyBird.Width-5, FlappyBird.Height);
            Canvas.SetTop(FlappyBird, Canvas.GetTop(FlappyBird) + gravity);

            if(Canvas.GetTop(FlappyBird) < -10 || Canvas.GetTop(FlappyBird) > 458)
            {
                EndGame();
            }

            foreach(var x in MyCanvas.Children.OfType<Image>())
            {
                if((string)x.Tag == "obs1" || (string)x.Tag == "obs2" || (string)x.Tag == "obs3")
                {
                    Canvas.SetLeft(x, Canvas.GetLeft(x) - 5);
                    if (Canvas.GetLeft(x) < -100)
                    {
                        Canvas.SetLeft(x, 800);
                        score += .5;
                    }

                    Rect pipeHitBox = new Rect(Canvas.GetLeft(x), Canvas.GetTop(x), x.Width, x.Height);

                    if (flappyBirdHitBox.IntersectsWith(pipeHitBox))
                    {
                        EndGame();
                    }
                }

                if((string)x.Tag == "cloud")
                {
                    Canvas.SetLeft(x, Canvas.GetLeft(x) - 1);
                    if (Canvas.GetLeft(x)<-250)
                    {
                        Canvas.SetLeft(x, 550);
                    }
                }
            }

        }

        private void KeyIsDown(object sender, KeyEventArgs e)
        {
            if(e.Key == Key.Space)
            {
                FlappyBird.RenderTransform = new RotateTransform(-20, FlappyBird.Width/2 , FlappyBird.Height/2);
                gravity = -8;
            }

            if (e.Key == Key.R && gameOver == true)
            {
                StartGame();
            }
        }

        private void KeyIsUp(object sender, KeyEventArgs e)
        {
            FlappyBird.RenderTransform = new RotateTransform(5, FlappyBird.Width / 2, FlappyBird.Height / 2);
            gravity = 8;
        }

        private void StartGame()
        {

            MyCanvas.Focus();

            int temp = 300;
            score = 0;
            gameOver = false;
            Canvas.SetTop(FlappyBird, 290);

            foreach(var x in MyCanvas.Children.OfType<Image>())
            {
                if ((string)x.Tag == "obs1")
                {
                    Canvas.SetLeft(x, 500);
                }
                if ((string)x.Tag == "obs2")
                {
                    Canvas.SetLeft(x, 800);
                }
                if ((string)x.Tag == "obs3")
                {
                    Canvas.SetLeft(x, 1100);
                }


                if ((string)x.Tag == "cloud")
                {
                    Canvas.SetLeft(x, 300 + temp);
                    temp = 800;
                }
            }

            gameTimer.Start();

        }

        private void EndGame()
        {
            gameTimer.Stop();
            gameOver = true;
            txtScore.Content += "Game Over !! Press R to try again.";
        }
    }
}
