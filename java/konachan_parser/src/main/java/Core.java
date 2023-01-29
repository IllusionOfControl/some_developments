import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URL;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;

/**
 * Created by ariki on 16.03.2017.
 */
public class Core {
    private final String SITE_URL =  "https://konachan.com/post/show/";
    private String site_url;
    private int imageValue;
    private int imageStart;
    private int statusCode;
    private int imageNumber;
    private String isDownload;
    private String imageName;
    private String imageURL;

    private Document document;
    private URL url;
    private ReadableByteChannel rbc;
    private FileOutputStream fos;
    private File image;

    //
    public void parsing() {
        try {
            document = Jsoup.connect(site_url).get();
            imageURL = document.body().select(".image").attr("src");
        } catch (IOException ioe) {}
    }

    //
    public void validation() {
        try {
            Connection.Response response = Jsoup.connect(site_url)
                                                .ignoreHttpErrors(true)
                                                .execute();
        statusCode = response.statusCode();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //
    public void download() {
            try {
                url = new URL( "http:" + site_url);
                rbc = Channels.newChannel(url.openStream());

                fos = new FileOutputStream(image);
                fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
                fos.close();
                fos.close();

                isDownload = "Yes";
            } catch (IOException e) {
                e.printStackTrace();
            }
    }

    //
    public void runUp() {
        for (imageNumber = imageStart; imageNumber <= (imageValue + imageStart); ++imageNumber)
            image = new File(imageName + "_" + imageNumber + ".jpg");
        if (!image.exists()) {
            validation();
            if (statusCode == 200) {
                parsing();
                if (!imageURL.equals("")) {
                    download();
                } else {isDownload = "No, image is not exists";}
            } else {isDownload = "No";}
        } else {isDownload = "No, image is exists";}
        print();
    }

    public void runDown() {
        for (imageNumber = imageStart; imageNumber <= (imageValue - imageStart); --imageNumber) {
            if (imageNumber == 0) break;
            image = new File(imageName + "_" + imageNumber + ".jpg");
            if (!image.exists()) {
                validation();
                if (statusCode == 200) {
                    parsing();
                    if (!imageURL.equals("")) {
                        download();
                    } else {
                        isDownload = "No, image is not exists";
                    }
                } else {
                    isDownload = "No";
                }
            } else {
                isDownload = "No, image is exists";
            }
            print();
        }
    }

    //
    public void init(int maxImage, int imageStart) {
        this.imageValue = imageValue + imageStart;
        this.imageStart = imageStart;
    }

    //
    public void print() {
        System.out.print("\nImage:\t" + imageNumber + "  Status Code:\t" + statusCode + "  Download:\t" + isDownload);
    }
}
