import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import javax.imageio.ImageWriter;
import javax.imageio.ImageWriteParam;
import javax.imageio.stream.MemoryCacheImageOutputStream;
import javax.imageio.IIOImage;
import java.io.ByteArrayOutputStream;
import java.io.ByteArrayInputStream;
import java.awt.Graphics2D;

public static class JPGEncoderV2 {
  
  private static BufferedImage removeAlphaChannel(BufferedImage img) {
    if (!img.getColorModel().hasAlpha()) {
        return img;
    }

    BufferedImage target = createImage(img.getWidth(), img.getHeight(), false);
    Graphics2D g = target.createGraphics();
    // g.setColor(new Color(color, false));
    g.fillRect(0, 0, img.getWidth(), img.getHeight());
    g.drawImage(img, 0, 0, null);
    g.dispose();

    return target;
  }

  private static BufferedImage createImage(int width, int height, boolean hasAlpha) {
      return new BufferedImage(width, height, hasAlpha ? BufferedImage.TYPE_INT_ARGB : BufferedImage.TYPE_INT_RGB);
  }

  byte[] encode(PImage img, float compression) throws IOException {
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    
    BufferedImage imgNoAlpha = removeAlphaChannel((BufferedImage) img.getNative());
    
    ImageWriter writer = ImageIO.getImageWritersByFormatName("jpeg").next();
    ImageWriteParam param = writer.getDefaultWriteParam();
    param.setCompressionMode(ImageWriteParam.MODE_EXPLICIT);
    param.setCompressionQuality(compression);

    // ImageIO.write((BufferedImage) img.getNative(), "jpg", baos);
    writer.setOutput(new MemoryCacheImageOutputStream(baos));

    writer.write(null, new IIOImage((BufferedImage) imgNoAlpha, null, null), param);

    return baos.toByteArray();
  }

  byte[] encode(PImage img) throws IOException {
    return encode(img, 0.5F);
  }

  PImage decode(byte[] imgbytes) throws IOException, NullPointerException {
    BufferedImage imgbuf = ImageIO.read(new ByteArrayInputStream(imgbytes));
    PImage img = new PImage(imgbuf.getWidth(), imgbuf.getHeight(), RGB);
    imgbuf.getRGB(0, 0, img.width, img.height, img.pixels, 0, img.width);
    img.updatePixels();

    return img; 
  }

}
