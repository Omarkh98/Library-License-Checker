import com.google.gson.Gson;
import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.junit.jupiter.api.Test;
import com.fasterxml.jackson.databind.ObjectMapper;
import okhttp3.OkHttpClient;

public class SampleTest {
    private static final Logger logger = LoggerFactory.getLogger(SampleTest.class);

    @Test
    public void testLoggingAndJson() {
        Gson gson = new Gson();
        ObjectMapper mapper = new ObjectMapper();
        OkHttpClient client = new OkHttpClient();

        String json = "{\"name\": \"HackBay\"}";
        try {
            Object obj = mapper.readValue(json, Object.class);
            logger.info("Parsed object: {}", gson.toJson(obj));
        } catch (Exception e) {
            logger.error("Failed to parse JSON", e);
        }
    }
}