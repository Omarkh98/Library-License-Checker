import
com.fasterxml.jackson.databind.
ObjectMapper; import
org.apache.commons.lang3.
StringUtils ;

public class MessyImportTest {
    public static void main(String[] args) {
        ObjectMapper mapper = new ObjectMapper();
        System.out.println(StringUtils.capitalize("hello"));
    }
}