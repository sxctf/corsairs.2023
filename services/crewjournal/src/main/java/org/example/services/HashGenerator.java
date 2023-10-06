package org.example.services;

import com.google.common.hash.*;
import org.example.model.Pirate;
import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.List;

public abstract class HashGenerator {
    static public String hashFrom(List<Pirate> pirateList){
        String piratesString = "";
        for(Pirate pirate: pirateList)
            piratesString += pirate.toString();
        HashFunction hf = Hashing.sha256();
        HashCode hc = hf.newHasher().putUnencodedChars(piratesString).hash();
        return hc.toString();
    }

    static public String hashFrom(String someString) {
        String sha ="";
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            md.update(someString.getBytes("UTF-8"));
            byte byteArr [] = md.digest();
            for(byte b: byteArr){
                String bHex = Integer.toHexString(0xff & b);
                sha += bHex.length() == 1?"0" + bHex:bHex;
            }
        } catch (NoSuchAlgorithmException | UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }
        return sha;
    }

    static public String myWeakHash(String data) throws UnsupportedEncodingException {
        if (data.length()==0)
            return "";
        byte originalBytes [] = data.getBytes("UTF-8");
        byte bytes [] = Arrays.copyOf(originalBytes, (originalBytes.length / 8 + 1) * 8);

        byte resultBytes [] = "CTF!B0dy".getBytes("UTF-8");
        for (int i = originalBytes.length; i < bytes.length; i++){
            bytes[i] = bytes[i - originalBytes.length];
        }
        for(int i = 0; i < bytes.length/8; i++){
            for (int j = 0; j < 8; j++){
                resultBytes[j]^=bytes[i*8+j];
            }
        }
        String result = "";
        for(byte b: resultBytes){
            String bHex = Integer.toHexString(0xff & b);
            result += bHex.length() == 1?"0" + bHex:bHex;
        }
        return result;
    }
}
