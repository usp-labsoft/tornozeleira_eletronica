package com.t100.tentativa_ummilhao;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Build;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.text.SimpleDateFormat;
import java.util.Date;

import android.os.AsyncTask;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.app.AlertDialog;
import android.app.AlertDialog;
/**
 * Classe para envio de dados via socket
 *
 * @author Thiago Galbiatti Vespa
 *
 */

public class MainActivity extends Activity {
    private Button btnSend;
    private TextView txtStatus;
    private TextView txtValor;
    private TextView txtHostPort;
    private TextView txtLocal;
    private SocketTask st;
    ObtainGPS gps;
    Button btLocalizacao;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        btnSend = (Button) findViewById(R.id.btnSend);
        txtStatus = (TextView) findViewById(R.id.txtStatus);
        txtValor = (TextView) findViewById(R.id.txtValor);
        txtHostPort = (TextView) findViewById(R.id.txtHostPort);
        txtLocal = (TextView) findViewById(R.id.txtLocal);
        btnSend.setOnClickListener(btnConnectListener);
        Location local;
        getLocalization();
        btLocalizacao = (Button) findViewById(R.id.button3);

        btLocalizacao.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getLocalization();
            }
        });
     /*   if ( ContextCompat.checkSelfPermission( this, android.Manifest.permission.ACCESS_COARSE_LOCATION ) != PackageManager.PERMISSION_GRANTED ) {

            ActivityCompat.requestPermissions( this, new String[] {  android.Manifest.permission.ACCESS_COARSE_LOCATION  },
                    LocationService.MY_PERMISSION_ACCESS_COURSE_LOCATION );
        }*/
       // Recupera host e porta
        final String host = "192.168.43.91";
        final String port = "8000";

        // Instancia a classe de conexão com socket
        st = new SocketTask(host, Integer.parseInt(port), 5000) {
            @Override
            protected void onProgressUpdate(String... progress) {
                SimpleDateFormat sdf = new SimpleDateFormat(
                        "dd/MM/yyyy HH:mm:ss");
                // Recupera o retorno
                txtStatus.setText(sdf.format(new Date()) + " - "
                        + progress[0]);
            }
        };

        st.execute("mandei"); // Envia os dados*/

    }
    public void getLocalization() {
        ObtainGPS gps = new ObtainGPS(MainActivity.this);



            // check if GPS enabled
            if (gps.canGetLocation()) {

                AlertDialog erroLocation = new AlertDialog.Builder(this).create();
                erroLocation.setTitle("Localização");
                erroLocation.setMessage("Lat:" + gps.getLatitude() + " Lng:" + gps.getLongitude());
                erroLocation.show();

            } else {

                AlertDialog erroLocation = new AlertDialog.Builder(this).create();
                erroLocation.setTitle("Localização não encontrada");
                erroLocation.setMessage("Sua Localização não foi encontrada!! Tente novamente!");
                erroLocation.show();
                gps.showSettingsAlert();
            }


    }

    public boolean GetLocalization(Context context) {
        int REQUEST_PERMISSION_LOCALIZATION = 221;
        boolean res = true;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                // TODO: Consider calling
                //    public void requestPermissions(@NonNull String[] permissions, int requestCode)
                // here to request the missing permissions, and then overriding
                //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                //                                          int[] grantResults)
                // to handle the case where the user grants the permission. See the documentation
                // for Activity#requestPermissions for more details.

                res = false;
                ActivityCompat.requestPermissions((Activity) context, new String[]{
                                Manifest.permission.ACCESS_FINE_LOCATION},
                        REQUEST_PERMISSION_LOCALIZATION);

            }
        }
        return res;
    }






    private View.OnClickListener btnConnectListener = new View.OnClickListener() {
        public void onClick(View v) {

            // Recupera host e porta
            String hostPort = txtHostPort.getText().toString();
            int idxHost = hostPort.indexOf(":");
            final String host = hostPort.substring(0, idxHost);
            final String port = hostPort.substring(idxHost + 1);

            // Instancia a classe de conexão com socket
            st = new SocketTask(host, Integer.parseInt(port), 5000) {
                @Override
                protected void onProgressUpdate(String... progress) {
                    SimpleDateFormat sdf = new SimpleDateFormat(
                            "dd/MM/yyyy HH:mm:ss");
                    // Recupera o retorno
                    txtStatus.setText(sdf.format(new Date()) + " - "
                            + progress[0]);
                }
            };

            st.execute(txtValor.getText() == null ? "" : txtValor.getText()
                    .toString()); // Envia os dado
        }
    };

    @Override
    protected void onDestroy() {
        super.onDestroy();
        st.cancel(true);
    }
}
