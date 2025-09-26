import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Button, Image, Platform, SafeAreaView, StyleSheet, Text, View } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

const WEB_UPLOAD_LABEL = 'Upload product image';
const NATIVE_UPLOAD_LABEL = 'Choose product image';

export default function App() {
  const [productImage, setProductImage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const fileInputRef = useRef<any>(null);
  const previousObjectUrlRef = useRef<string | null>(null);

  useEffect(() => {
    return () => {
      if (previousObjectUrlRef.current) {
        URL.revokeObjectURL(previousObjectUrlRef.current);
      }
    };
  }, []);

  const handleWebFileChange = useCallback((event: any) => {
    const file = event?.target?.files?.[0];

    if (!file) {
      return;
    }

    if (previousObjectUrlRef.current) {
      URL.revokeObjectURL(previousObjectUrlRef.current);
      previousObjectUrlRef.current = null;
    }

    const objectUrl = URL.createObjectURL(file);
    previousObjectUrlRef.current = objectUrl;

    setErrorMessage(null);
    setProductImage(objectUrl);
  }, []);

  const handlePickImageNative = useCallback(async () => {
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (permissionResult.status !== 'granted') {
      setErrorMessage('Permission to access gallery is required to upload a product image.');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });

    if (result.canceled) {
      return;
    }

    const asset = result.assets?.[0];
    if (asset?.uri) {
      setErrorMessage(null);
      setProductImage(asset.uri);
    }
  }, []);

  const handlePickImage = useCallback(() => {
    if (Platform.OS === 'web') {
      setErrorMessage(null);
      const inputElement = fileInputRef.current;
      if (!inputElement) {
        return;
      }

      inputElement.click();
      return;
    }

    void handlePickImageNative();
  }, [handlePickImageNative]);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Add a new product</Text>
        <Text style={styles.description}>
          {Platform.OS === 'web'
            ? 'Upload an image directly from your computer to see a preview before saving.'
            : 'Choose an image from your gallery to include it with your product.'}
        </Text>
        <View style={styles.buttonContainer}>
          <Button
            title={Platform.OS === 'web' ? WEB_UPLOAD_LABEL : NATIVE_UPLOAD_LABEL}
            onPress={handlePickImage}
          />
          {Platform.OS === 'web' && (
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              style={{ display: 'none' }}
              onChange={handleWebFileChange}
            />
          )}
        </View>
        {errorMessage && <Text style={styles.error}>{errorMessage}</Text>}
        {productImage && (
          <Image source={{ uri: productImage }} style={styles.previewImage} resizeMode="cover" />
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 24,
    gap: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
    textAlign: 'center',
  },
  description: {
    fontSize: 16,
    color: '#444',
    textAlign: 'center',
  },
  buttonContainer: {
    width: '100%',
    maxWidth: 320,
  },
  error: {
    color: '#b00020',
    fontSize: 14,
  },
  previewImage: {
    width: 240,
    height: 240,
    borderRadius: 12,
  },
});

